# Generated by Django 4.1.1 on 2022-11-24 07:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fileapp', '0007_alter_customer_email'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
    ]