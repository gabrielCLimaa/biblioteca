# Generated by Django 4.0.1 on 2022-01-15 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BookInstace',
            new_name='BookInstance',
        ),
    ]
