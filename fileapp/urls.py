from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    password_generator,
    password_generator_api,

    encrypt_file, simple_upload,
    file_information,
    file_to_xml,
    download_zip_folder,
    download_youtube_videos,
    test_api,
    get_countries,
    get_cities,
    update_customer,
    delete_customer,
    donate,
    handle_donation,
    course_registration,
    student_registration,
    school_registration,
    course_details,

    CustomerViewSet,
    HouseOwnerViewSet,
    HouseImageViewSet,
    HouseViewSet,
    DonateViewSet,
)

app_name = 'fileapp'

router = DefaultRouter()
router.register('customer', CustomerViewSet)
router.register('house-owner', HouseOwnerViewSet)
router.register('house-image', HouseImageViewSet)
router.register('house', HouseViewSet)
router.register('donate', DonateViewSet)


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('password_generator_api/',
         password_generator_api),

    path('password_generator/',
         password_generator,
         name='password_generator'),

    path('course_details/<str:course_code>/',
         course_details, name='course_details'),
    path('school_registration/', school_registration,
         name='school_registration'),
    path('student_registration/', student_registration,
         name='student_registration'),
    path('course_registration/', course_registration,
         name='course_registration'),
    path('handle_donation/', handle_donation),
    path('donate/', donate, name='donate'),
    path('delete_customer/', delete_customer),
    path('update_customer/', update_customer),
    path('get_cities/<str:country_name>/', get_cities),
    path('get_countries/', get_countries),
    path('test_api/', test_api),
    path('download_youtube_videos/', download_youtube_videos,
         name='download_youtube_videos'),
    path('download_zip_folder/', download_zip_folder,
         name='download_zip_folder'),
	path('file_to_xml/', file_to_xml,
		 name='file_to_xml'),
    path('file_information/', file_information,
         name='file_information'),
    path('encrypt_file/', encrypt_file, 
         name='encrypt_file'),
    path('simple_upload/', simple_upload,
         name='simple_upload'),
]