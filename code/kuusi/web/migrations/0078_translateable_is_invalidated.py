# Generated by Django 4.2.4 on 2023-09-23 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0077_remove_facette_is_invalidated"),
    ]

    operations = [
        migrations.AddField(
            model_name="translateable",
            name="is_invalidated",
            field=models.BooleanField(default=False),
        ),
    ]
