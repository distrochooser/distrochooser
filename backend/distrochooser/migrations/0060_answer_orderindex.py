# Generated by Django 2.2.20 on 2021-04-25 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distrochooser', '0059_usersession_remarksprocessed'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='orderIndex',
            field=models.IntegerField(default=0),
        ),
    ]
