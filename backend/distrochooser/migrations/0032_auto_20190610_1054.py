# Generated by Django 2.1.2 on 2019-06-10 08:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distrochooser', '0031_auto_20190609_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='distribution',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='usersession',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 10, 10, 54, 58, 38189)),
        ),
    ]