# Generated by Django 4.2.4 on 2023-08-29 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0074_translationsuggestion"),
    ]

    operations = [
        migrations.AddField(
            model_name="translationsuggestion",
            name="amount",
            field=models.IntegerField(default=0),
        ),
    ]
