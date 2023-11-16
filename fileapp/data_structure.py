import json
from datetime import datetime


def raise_on_error(message, instance, parent):
	if not isinstance(instance, parent):
		raise Exception(message)

class General:
	def __init__(self, name):
		self.name = name

class School(General):
	SCHOOLS = []
	def __init__(self, name, location):
		super().__init__(name)
		# for school in School.SCHOOLS:
		# 	if school.name == name:
		# 		raise Exception('school is already registered.')
		self.location = location
		School.SCHOOLS.append(self)

	def get_schools(self):
		data = json.dumps({
			'schools': [json.loads(str(school)) for school in School.SCHOOLS]
		}, indent=4)
		with open('schools.json', 'w') as f:
			f.write(data)
		return data

	def __str__(self):
		return json.dumps({
			'name': self.name,
			'location': self.location
		})

# utp = School('Universiti Teknologi Petronas', 'Seri Iskandar, Perak, Malaysia')
# uem = School('Universidade Eduardo Mondlane', 'Maputo')
# # utp = School('Universiti Teknologi Petronas', 'Seri Iskandar, Perak, Malaysia')
# utp.get_schools()



class Subject(General):
	COURSES = []
	def __init__(self, name, code):
		super().__init__(name)
		# for subject in Subject.COURSES:
		# 	if subject.name == name or subject.code == code:
		# 		raise Exception('course is already registered')
		self.code = code
		self.course_hours = 0
		Subject.COURSES.append(self)

	def get_subjects(self):
		data = json.dumps({
			'subjects': [json.loads(str(subj)) for subj in Subject.COURSES]
		}, indent=4)
		with open('subjects.json', 'w') as f:
			f.write(data)
		return data

	def __str__(self):
		return json.dumps({
			'name': self.name,
			'code': self.code,
			'course_hours': self.course_hours
		}, default=str)

# with open('subjects.json') as f:
# 	subjects = json.loads(f.read())
# 	subjects = subjects['subjects']
# codes = [subj['code'] for subj in subjects]
# print(codes)

# math = Subject('Math', 'AB24')
# chemistry = Subject('Chemistry', 'AB43')
# english = Subject('English', 'AB23')
# print(math.get_subjects())

# with open('subjects.json') as f:
# 	data = f.read()
# print(json.loads(data))

# chemistry = Subject('Math', 'AB43')


class Person(General):
	def __init__(self, name, email):
		super().__init__(name)
		self.email = email

def add_instances(message, parent, instances):
	values = []
	for instance in instances:
		raise_on_error(message, instance, parent)
		values.append(instance)
	return values

def format_date(obj):
	if isinstance(obj, datetime):
		return obj.isoformat()
	return obj

class Student:
	STUDENTS = []
	def __init__(self, first_name, last_name, email, date_of_birth, school, subjects=[]):
		# super().__init__(name, email)
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.date_of_birth = date_of_birth
		if not isinstance(school, School):
			raise Exception('school must be an instance of School class')
		self.school = school
		self.subjects = add_instances('subject must an instance of Subject class', Subject,
									  subjects)
		for student in Student.STUDENTS:
			if student.email == email:
				raise Exception('student is already registered.')
		Student.STUDENTS.append(self)

	def get_students(self):
		data = json.dumps({
			'students': [json.loads(str(stud)) for stud in Student.STUDENTS]
		}, indent=4)
		with open('students.json', 'w') as f:
			f.write(data)
		return data

	def __str__(self):
		return json.dumps({
			'first_name': self.first_name,
			'last_name': self.last_name,
			'email': self.email,
			'date_of_birth': self.date_of_birth,
			'school': json.loads(str(self.school)),
			'subjects': [json.loads(str(subject)) for subject in self.subjects]
		}, default=format_date)


# oop = Subject('Object Oriented Programming', 'AB21')
# st1 = Student('Januario', 'janu@example.com', 27, utp,
# 			 [math, chemistry])
# st2 = Student('Manuel', 'manuel@example.com', 27, uem,
# 			 [english, oop])
# print(st2)


class Teacher(Person):
	def __init__(self, name, email, subjects=[], students=[]):
		super().__init__(name, email)
		self.subjects = add_instances('subject must an instance of Subject class', Subject,
								      subjects)
		self.students = add_instances('subject must an instance of Subject class', Student,
								      students)

	def __str__(self):
		return json.dumps({
			'name': self.name,
			'email': self.email,
			'subjects': [json.loads(str(subject)) for subject in self.subjects],
			'students': [json.loads(str(student)) for student in self.students]
		})


# tea = Teacher('Americo', 'americo@utp.edu.my',
# 			  [math, chemistry], [st1, st2])
# print(json.loads(str(tea)))


class CourseRegistration:
	REGISTRATIONS = []
	def __init__(self, student, school, subject):
		raise_on_error('student must an instance of Student class', student, Student)
		self.student = student
		raise_on_error('school must an instance of School class', school, School)
		self.school = school
		raise_on_error('subject must an instance of Subject class', subject, Subject)
		self.subject = subject
		CourseRegistration.REGISTRATIONS.append(self)

	def __str__(self):
		return json.dumps({
			'student': json.loads(str(self.student))
		})


# course_reg1 = CourseRegistration(st1, utp, math)
# course_reg2 = CourseRegistration(st1, utp, english)
# course_reg2 = CourseRegistration(st1, utp, chemistry)
# for reg in course_reg1.REGISTRATIONS:
# 	print(reg)
# 	print()