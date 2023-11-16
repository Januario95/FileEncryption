from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from win32com.client.gencache import EnsureDispatch
from rest_framework.viewsets import ModelViewSet

from django.views.decorators.http import (
    require_POST
)
from rest_framework.decorators import api_view
from django.middleware.csrf import get_token

import os
import json
import awoc
from pathlib import Path
import aspose.words as aw
from random import randint
from pytube import YouTube
import requests, zipfile, io
from datetime import datetime
from countryinfo import CountryInfo

from .models import (
    FileEncryption,
    Customer,
    HouseOwner,
    HouseImage,
    House, 
    Donate, 
)
from .serializers import (
    CustomerSerializer,
    HouseOwnerSerializer,
    HouseImageSerializer,
    HouseSerializer,
    DonateSerializer,
)
from .data_structure import (
    Subject, School, Student,
)
from .forms import (
    PasswordGeneratorForm,
    EncryptionForm, # FileEncryptionForm
    FileInformation,
    DownloadZipFolderForm,
    DonateForm,
    SubjectForm,
    StudentForm,
    SchoolForm,
)
from .helpers import (
    DataFrameToXML, get_password
)

@api_view(['POST',])
def password_generator_api(request):
    data = json.loads(request.body)
    try:
        min_length = int(data.get('pass_min_length'))
        max_length = int(data.get('pass_max_length'))
        if max_length < min_length:
            password = ''
            status = 'Error'
            reason = 'Max length must be greater than minimum length'
        else:
            password = get_password(maximum=max_length)
            status = 'Success'
            reason = ''
    except Exception as e:
        password = ''
        status = 'Error'
        reason = e.args

    return JsonResponse({
        'password': password,
        'status': status,
        'reason': reason
    })


def password_generator(request):
    password = ''
    # if request.method == 'POST':
    #     form = PasswordGeneratorForm(
    #         request.POST)
    #     if form.is_valid():
    #         data = form.cleaned_data
    #         min_length = int(data.get('pass_min_length'))
    #         max_length = int(data.get('pass_max_length'))
    #         password = get_password(max_length)
    #     else:
    #         print(form.errors)
    # else:
    #     form = PasswordGeneratorForm()

    form = PasswordGeneratorForm()

    return render(request,
                  'files/password_generator.html',
                  {'form': form,
                   'password': password})



def get_schools():
    try:
        with open('schools.json') as f:
            schools = json.loads(f.read())
        schools = schools['schools']
    except Exception as e:
        schools = []
    return schools

def get_subjects():
    try:
        with open('subjects.json') as f:
            subjects = json.loads(f.read())
        subjects = subjects['subjects']
    except Exception as e:
        subjects = []
    return subjects

def get_students():
    try:
        with open('students.json') as f:
            students = json.loads(f.read())
        students = students['students']
        for student in students:
            student['date_of_birth'] = datetime.strptime(student['date_of_birth'], '%Y-%m-%dT%H:%M:%S')
    except Exception as e:
        students = []
    return students

def extract_subject(element, code):
    subjects = get_subjects()
    subjs = []
    if element:
        for subj in subjects:
            if subj['code'] == code:
                return subj
    return None

def course_details(request, course_code):
    subjects = get_subjects()
    subject = None
    for subj in subjects:
        if subj['code'] == course_code:
            subject = subj
            print(subject)

    return render(request,
                  'files/course_details.html',
                  {'subject': subject})

def student_registration(request):
    schools = get_schools()
    subjects = get_subjects()
    students = get_students()

    regi_error = False
    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        date_of_birth = request.POST.get('date-of-birth')
        date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d')
        # print(f'date_of_birth = {type(date_of_birth)}')
        school = request.POST.get('school')
        schools = get_schools()
        for sch in schools:
            if sch['name'] == school:
                school = School(sch['name'], sch['location'])

        codes = [subj['code'] for subj in subjects]
        subjs = []
        for code in codes:
            element = request.POST.get(code)
            subj = extract_subject(element, code)
            if subj:
                course_hours = subj['course_hours']
                del subj['course_hours']
                subj = Subject(**subj)
                subj.course_hours = course_hours
                subjs.append(subj)

        try:
            student = Student(first_name, last_name, email, date_of_birth, school, subjs)
            student.get_students()
            print(student)
        except Exception as e:
            print(e)
            regi_error = True

        students = get_students()
    return render(request,
                  'files/student_registration.html',
                  {'schools': schools, 'subjects': subjects,
                   'students': students, 'regi_error': regi_error})

def school_registration(request):
    # token = get_token(request)
    # print(f'token = {token}')
    # print(settings.LANGUAGES)

    try:
        with open('schools.json') as f:
            schools = json.loads(f.read())
        schools = schools['schools']
    except Exception as e:
        schools = []
    # print(schools)

    regi_error = False
    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            location = data['location']

            try:
                school = School(name, location)
                schools = json.loads(school.get_schools())
                schools = schools['schools']
                print(schools)
            except Exception as e:
                regi_error = True
                print(e)
        else:
            print(form.errors)
    else:
        form = SchoolForm()

    return render(request,
                  'files/school_registration.html',
                  {'form': form, 'schools': schools,
                   'regi_error': regi_error})

def course_registration(request):
    subject = None
    # subjects = Subject.COURSES
    try:
        with open('subjects.json') as f:
            subjects = json.loads(f.read())
        subjects = subjects['subjects']
    except Exception as e:
        subjects = []

    regi_error = False
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            code = data['code']
            course_hours = data['course_hours']
            try:
                subject = Subject(name, code)
                subject.course_hours = course_hours
                subjects = json.loads(subject.get_subjects())
                subjects = subjects['subjects']
            except Exception as e:
                regi_error = True
                print(e)
    else:
        form = SubjectForm()
    return render(request,
                  'files/course_registration.html',
                  {'form': form, 'subject': subject,
                   'subjects': subjects, 'regi_error': regi_error})


@api_view(['POST',])
def handle_donation(request):
    data = json.loads(request.body)
    name = data['name']
    country = data['country']
    card_number = data['card_number']
    expiration = data['expiration']
    amount = data['amount']

    data = {
        'name': name, 'country': country,
        'card_number': card_number,
        'expiration': expiration,
        'amount': amount,
    }

    donation = Donate.objects.create(
        name=name, country=country,
        card_number=card_number,
        expiration=expiration, amount=amount
    )
    donation.save()
    last = Donate.objects.last()
    data['last_id'] = last.id
    print(json.dumps(data, indent=4))

    return JsonResponse(data)

def donate(request):
    # form = DonateForm()
    donations = Donate.objects.all()

    return render(request,
                  'files/donate.html',
                   {'donations': donations})

class DonateViewSet(ModelViewSet):
    queryset = Donate.objects.all()
    serializer_class = DonateSerializer


class HouseOwnerViewSet(ModelViewSet):
    queryset = HouseOwner.objects.all()
    serializer_class = HouseOwnerSerializer

class HouseImageViewSet(ModelViewSet):
    queryset = HouseImage.objects.all()
    serializer_class = HouseImageSerializer

class HouseViewSet(ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer


def get_cities(request, country_name):
    country = CountryInfo(country_name)
    info = {}
    exists = False
    try:
        info = country.info()
        exists = True
    except KeyError as e:
        pass

    return JsonResponse({
        'cities': info.get('provinces'),
        'exists': exists
    })


def get_countries(request):
    world = awoc.AWOC()
    countries = [country['Country Name'] for country
                 in world.get_countries()]

    return JsonResponse({
        'countries': countries
    })

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


@api_view(['POST',])
def delete_customer(request):
    data = json.loads(request.body)
    clientId = data['clientId']
    deleted = False
    client = Customer.objects.filter(id=clientId)
    if client.exists():
        client = client.first()
        client.delete()
        deleted = True

    return JsonResponse({
        'deleted': deleted
    })

@api_view(['POST',])
def update_customer(request):
    data = json.loads(request.body)
    email=data['email']

    client = Customer.objects.filter(
        email=email
    )
    updated = False
    if client.exists():
        client = client.first()
        client.first_name=data['firstName']
        client.last_name=data['lastName']
        client.city=data['city']
        client.country=data['country']
        client.save()
        updated = True

    return JsonResponse({
        'customer': data
    })


@api_view(['POST',])
def test_api(request):
    data = json.loads(request.body)
    customer = Customer.objects.filter(
        email=data['email']
    )
    exists = False
    if customer.exists():
        print(customer)
        exists = True
    else:
        customer = Customer.objects.create(
            first_name=data['firstName'],
            last_name=data['lastName'],
            email=data['email'],
            city=data['city'],
            country=data['country']
        )
        customer.save()

    return JsonResponse({
        'exists': exists
    })

def Download(link):
    os.chdir('C:/Users/a248433/Downloads')
    youtubeObject = YouTube(link)
    print(youtubeObject.title)
    file_path = os.getcwd() + "\\" + youtubeObject.title + '.mp4'
    print(file_path)
    path = Path(file_path)
    if path.exists():
        pass
    else:
        try:
            youtubeObject = youtubeObject.streams.get_highest_resolution()
            youtubeObject.download()
        except Exception as e:
            raise e
    print("Download is completed successfully")



def download_youtube_videos(request):
    if request.method == 'POST':
        form = DownloadZipFolderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            url = data['url']
            Download(url)
    else:
        form = DownloadZipFolderForm()

    return render(request,
                  'files/download_youtube_videos.html',
                  {'form': form})


def download_zip_folder(request):
    if request.method == 'POST':
        form = DownloadZipFolderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            url = data['url']

            r = requests.get(url)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            filename = 'C:/Users/a248433/Downloads/' + url.split('/')[-1]
            print(filename)
            file_path = Path(filename)
            z.extractall(filename)
            # print(file_path.exists())

    else:
        form = DownloadZipFolderForm()

    return render(request,
                  'files/download_zip_folder.html',
                  {'form': form})


def file_to_xml(request):
    data = None
    if request.method == 'POST':
        form = FileInformation(request.POST,
                               request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            file = data['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            # print(dir(filename))

            path = os.path.abspath('media/')
            entries = Path(path)

            for entry in entries.iterdir():
                if entry.is_file():
                    if entry.name == file.name:
                        file_exists = os.path.exists(os.path.join('media/', file.name))
                        if file_exists:
                            filename = os.path.join('media/', file.name)
                            df_to_xml = DataFrameToXML(filename)
                            filename = filename.split('/media/')[0].split('media/')[-1].split('.')[0]
                            xml = df_to_xml.create_xml(filename)

                            data = xml.toprettyxml() # df_to_xml.data
                            print(data)
            
    else:
        form = FileInformation()

    return render(request,
                  'files/file_to_xml.html',
                  {'form': form,
                   'data': data})

def format_time(time):
    utc = datetime.utcfromtimestamp(time)
    formatted = utc.strftime('%d %b %Y %H:%M:%S')
    return formatted


def file_information(request):
    data = {}
    file_is_processed = False
    if request.method == 'POST':
        form = FileInformation(request.POST,
                               request.FILES)
        if form.is_valid():
            path = os.path.abspath('media/')
            entries = Path(path)
            
            data = form.cleaned_data
            file = data['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            # f = open(fs.path(file.name), 'rb').read()
            
            for entry in entries.iterdir():
                if entry.is_file():
                    if entry.name == file.name:
                        data['name'] = entry.name
                        info = entry.stat()
                        data['file_mode'] = info.st_mode
                        data['creation_time'] = format_time(info.st_ctime)
                        data['last_access_time'] = format_time(info.st_atime)
                        data['size'] = info.st_size
                        file_is_processed = True
    else:
        form = FileInformation()
        
    return render(request,
                  'files/file_information.html',
                  {'form': form,
                   'data': data,
                   'file_is_processed': file_is_processed})



def simple_upload(request):
    if request.method == 'POST':
        print(request.FILES)
        file = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        print('=============')
        print(uploaded_file_url)
        print('=============')
        return HttpResponse(uploaded_file_url)
        # return render(request,
        #               'files/simple_upload.html',
        #               {'uploaded_file_url': uploaded_file_url})

    return render(request,
                  'files/simple_upload.html')


def encrypt_word_doc(filename, password):
    # load document
    doc = aw.Document(filename)
    
    # create document options
    options = aw.saving.OoxmlSaveOptions(aw.SaveFormat.DOCX)
    
    # set password
    options.password = password
    
    # save updated document
    doc.save(filename, options)
    
    
def encrypt_excel_file(filename, password):
    app = EnsureDispatch("Excel.Application")
    excel_file = app.Workbooks.Open(filename)
    app.DisplayAlerts = False
    excel_file.Visible = False
    excel_file.SaveAs(filename, Password = 'Jaci1995')
    excel_file.Close()
    app.Quit()



def encrypt_file(request):
    if request.method == 'POST':
        form = EncryptionForm(request.POST, request.FILES)
        # form = FileEncryptionForm(request.POST, request.FILES)
        if form.is_valid():
            
            data = form.cleaned_data
            password = data['password']
            file = data['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_ = os.getcwd() + "\\media\\" + filename
            
            filetype = None
            if file.name[-5:] == '.docx':
                uploaded_file_url = fs.url(filename)
                encrypt_word_doc(file_, password)
                
                obj = FileEncryption.objects.create(
                    password=password,
                    filename=uploaded_file_url.split('/media/')[1]
                )
            elif file.name[-5:] == '.xlsx':
                uploaded_file_url = fs.url(filename)
                encrypt_excel_file(file_, password)
                
                obj = FileEncryption.objects.create(
                    password=password,
                    filename=uploaded_file_url.split('/media/')[1]
                )
            else:
                uploaded_file_url = None
                filetype = 'File type not supported! Supported files: .docx, .xlsx'
                
            form = EncryptionForm()
            return render(request,
                              'files/encrypt_file.html',
                              {'uploaded_file_url': uploaded_file_url,
                               'filetype': filetype,
                               'form': form})
        else:
            print(form.errors)
    else:
        form = EncryptionForm()
        # form = FileEncryptionForm()
        
    return render(request,
                  'files/encrypt_file.html',
                  {'form': form})


































