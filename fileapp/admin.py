from django.contrib import admin
from django.utils.safestring import mark_safe

import os

from .models import (
    FileEncryption, 
    Customer,
    HouseOwner,
    HouseImage,
    House,
    Donate,
)


@admin.register(Donate)
class DonateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'country',
                    'card_number', 'expiration', 'amount',
                    'created_at', 'updated_at']

@admin.register(HouseOwner)
class HouseOwnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 
                    'created_at', 'updated_at']

@admin.register(HouseImage)
class HouseImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_name', 'show_image',
                    'created_at', 'updated_at']

    def show_image(self, obj):
        return mark_safe(f'''
            <a href="{obj.image.url}" target="_blank">
                <img src="{obj.image.url}"
                    width="100px" height="110px" />
            </a>
        ''')
    show_image.short_description = 'Image Name'

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ['id', 'bairro', 'city',
                    'rooms', 'price', 'owner', 'show_houses',
                    'created_at', 'updated_at']
    list_display_links = ['id', 'bairro']
    list_editable = ['price', 'rooms']

    def show_houses(self, obj):
        image_urls = [img.image.url for img in obj.images.all()]
        urls = mark_safe(f'''
            <a href="{image_urls[0]}"  target="_blank">
                <img src="{image_urls[0]}"
                    width="100px" height="110px" 
                    style="border:1px solid #ccc; margin:5px;
                          border-radius:50%; padding: 5px;"
                />
            </a>
        ''')
        for url in image_urls[1:]:
            urls += mark_safe(f'''
                <a href="{url}" target="_blank">
                    <img src="{url}"
                        width="100px" height="110px" 
                        style="border:1px solid #ccc; margin:5px;
                               border-radius:50%; padding: 5px;"
                    />
                </a>
            ''')
        return urls

    show_houses.short_description = 'Show Houses'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ['id', 'first_name', 'last_name',
					'email', 'city', 'country',
                    'created_at', 'updated_at']
	

@admin.register(FileEncryption)
class FileEncryptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'password', 'filename_',
                    'created_at', 'updated_at']
    
    def filename_(self, obj):
        file = obj.filename
        # file_ = os.getcwd() + "\\media\\" + file
        return file #  mark_safe(f'''<a href="{file_}" target="_blank">{file_}</a>''')
    filename_.short_description = 'Filename'




