# Generated by Django 4.1.1 on 2022-12-07 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student_app', '0009_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
