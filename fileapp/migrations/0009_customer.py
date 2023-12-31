# Generated by Django 4.1.1 on 2022-11-24 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileapp', '0008_delete_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=125)),
                ('last_name', models.CharField(max_length=125)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('city', models.CharField(max_length=125)),
                ('country', models.CharField(max_length=125)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
                'ordering': ('first_name',),
            },
        ),
    ]
