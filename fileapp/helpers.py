import csv
import string
import random
import sqlite3
import pandas as pd
from glob import glob
from random import choice
import xml.dom.minidom as minidom

conn = sqlite3.Connection('actors_movies.sql')

EXTENSIONS = {
	'csv': lambda filename: pd.read_csv(filename),
	'xlsx': lambda filename: pd.read_excel(filename),
	'json': lambda filename:  pd.read_json(filename),
	'hdf': lambda filename: pa.read_hdf(filename),
	'p': lambda filename: pd.read_pickle(filename),
	'sas': lambda filename: pd.read_sas(filename),
	'spss': lambda filename: pd.read_spss(filename),
	'sql': lambda filename, con: pd.read_sql(filename, con=conn),
	'stata': lambda filename: pd.read_stata(filename),
	'xml': lambda filename: pd.read_xml(filename)
}

class DataFrameToXML:
	def __init__(self, filename):
		file_extension_reader = EXTENSIONS.get(filename.split('.')[-1])
		if file_extension_reader:
			self.df = file_extension_reader(filename)
			self.tree = minidom.Document()
		else:
			raise FileNotFoundError(f"No such file or directory: '{filename}'")


	@property
	def data(self):
		data_ = []
		for row in self.df.iterrows():
			indexes = row[1].index.tolist()
			values = row[1].values
			data_.append(dict(zip(indexes, values)))
		return data_

	def create_row(self, subtree, row, tag_name):
		main = self.tree.createElement(tag_name[:-1])
		for key, value in row.items():
			tag = self.tree.createElement(str(key))
			tag.setAttribute('value', str(value))
			main.appendChild(tag)

		subtree.appendChild(main)

	def create_xml(self, root_name):
		self.tree = minidom.Document()
		presidents = self.tree.createElement(root_name)
		self.tree.appendChild(presidents)
		
		for row in self.data:
			self.create_row(presidents, row, root_name)
		return self.tree


# df_to_xml = DataFrameToXML(filename)
# xml = df_to_xml.create_xml(filename)
# print(xml.toprettyxml())



chars = string.ascii_letters + \
		string.digits + \
		"$%&@\\<=>?{|}~()+"

letters = [char for char in chars]

def shuffle():
	global letters
	random.shuffle(letters)

def get_password(n=100, maximum=12):
	for _ in range(n):
		shuffle()

	min_val = random.randint(0, len(letters)-1)
	password = ''.join(letters)[min_val:min_val+maximum]
	first = password[0]
	if password[0].isdigit():
		return random.choice(string.ascii_letters) + password[1:]
	else:
		return password
	









