# Generated by Django 2.2.10 on 2020-03-30 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distrochooser', '0054_auto_20200330_2014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersession',
            name='isPending',
        ),
        migrations.AddField(
            model_name='usersession',
            name='calculationTime',
            field=models.IntegerField(default=0),
        ),
    ]
