# Generated by Django 4.1.3 on 2022-11-03 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileEncryption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='')),
            ],
            options={
                'verbose_name': 'File Encryption',
                'verbose_name_plural': 'File Encryptions',
            },
        ),
    ]
