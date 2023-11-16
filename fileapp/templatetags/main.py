from django.template import library


library = library.Library()


@library.simple_tag()
def format_xml(data):
	return 'Me'

