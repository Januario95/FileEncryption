from django.db import models

from .country_list import Country

class Donate(models.Model):
    name = models.CharField(max_length=125)
    country = models.CharField(max_length=50,
        choices=Country, default='Mozambique')
    card_number = models.CharField(max_length=16)
    expiration = models.CharField(max_length=50)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.country} - {self.amount}'

    class Meta:
        ordering = ('id',)
        verbose_name  = 'Donation'
        verbose_name_plural = 'Donations'


class HouseOwner(models.Model):
    name = models.CharField(max_length=125)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class HouseImage(models.Model):
    image_name = models.CharField(max_length=125)
    image = models.ImageField(upload_to='house-images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image_name


class House(models.Model):
    bairro = models.CharField(max_length=125)
    city = models.CharField(max_length=125)
    rooms = models.IntegerField()
    price = models.DecimalField(decimal_places=2,
        max_digits=10, default=1000.00)
    owner = models.ForeignKey(to=HouseOwner,
                              on_delete=models.CASCADE)
    images = models.ManyToManyField(to=HouseImage)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.owner.name} - {self.bairro}:{self.city}:{self.rooms}'
    




class Customer(models.Model):
    first_name = models.CharField(max_length=125)
    last_name = models.CharField(max_length=125)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=125)
    country = models.CharField(max_length=125)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ('first_name',)
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class FileEncryption(models.Model):
    password = models.CharField(max_length=100)
    filename = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    # file = models.FileField()
    
    def __str__(self):
        return f'{self.filename}' #  '.name}'
    
    class Meta:
        verbose_name = 'File Encryption'
        verbose_name_plural = 'File Encryptions'
        


