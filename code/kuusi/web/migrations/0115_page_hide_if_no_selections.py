# Generated by Django 4.2.4 on 2024-07-28 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0114_remove_session_filter_string"),
    ]

    operations = [
        migrations.AddField(
            model_name="page",
            name="hide_if_no_selections",
            field=models.BooleanField(default=False),
        ),
    ]