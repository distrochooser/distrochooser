# Generated by Django 2.2.3 on 2019-12-13 15:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distrochooser', '0045_auto_20191213_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersession',
            name='isPending',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='usersession',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 13, 16, 19, 53, 340772)),
        ),
    ]