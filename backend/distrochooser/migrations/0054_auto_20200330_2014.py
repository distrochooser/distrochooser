# Generated by Django 2.2.10 on 2020-03-30 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('distrochooser', '0053_auto_20200208_1151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersession',
            name='checksDone',
        ),
        migrations.RemoveField(
            model_name='usersession',
            name='checksToDo',
        ),
    ]
