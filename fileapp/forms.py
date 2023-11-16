from django import forms

from .models import (
	Donate,
    # FileEncryption    
)


class PasswordGeneratorForm(forms.Form):
    pass_min_length = forms.CharField(
        max_length=1,
        widget=forms.NumberInput(attrs={
            'value': 6
        }))
    pass_max_length = forms.CharField(
        min_length=1,
        max_length=2,
        widget=forms.NumberInput(attrs={
            'value': 12
        }))


class StudentForm(forms.Form):
    name = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={
            'placeholder': 'Enter your first name',
            'value': 'Math'
        }))
    name = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={
            'placeholder': 'Enter your last name',
            'value': 'Math'
        }))
    email = forms.EmailField(
        max_length=150, widget=forms.TextInput(attrs={
            'placeholder': 'Enter subject name',
            'value': 'Math'
        }))
    birth_date = forms.DateField()
    school = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={
            'placeholder': 'Enter subject name',
            'value': 'Math'
        }))

class SchoolForm(forms.Form):
    name = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={
            'placeholder': 'Enter school name',
            'value': 'Universiti Teknologi Petronas',
            'style': 'width: 200px; height: 33px;'
        }))
    location = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={
            'placeholder': 'Enter school location',
            'value': 'Seri Iskandar, Perak, Malaysia',
            'style': 'width: 200px; height: 33px;'
        }))


class SubjectForm(forms.Form):
    name = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={
            'placeholder': 'Enter subject name',
            'value': 'Math'
        }))
    code = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={
            'placeholder': 'Enter subject code',
            'value': 'AB24'
        }))
    course_hours = forms.DecimalField(widget=forms.TextInput(attrs={
        'value': 25.5
    }))

class DonateForm(forms.ModelForm):
	class Meta:
		model = Donate
		fields = '__all__'


# class FileEncryptionForm(forms.ModelForm):
#     class Meta:
#         model = FileEncryption
#         fields = '__all__'


class DownloadZipFolderForm(forms.Form):
	url = forms.CharField()


class FileInformation(forms.Form):
    file = forms.FileField()


class EncryptionForm(forms.Form):
    password = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
           
        })
    )
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
    




    
    