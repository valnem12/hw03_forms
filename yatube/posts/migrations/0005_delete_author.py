# Generated by Django 2.2.9 on 2021-11-16 01:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_author'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Author',
        ),
    ]
