# Generated by Django 4.2.4 on 2023-08-24 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0061_alter_facetteselectionwidget_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="page",
            name="can_be_marked",
            field=models.BooleanField(default=False),
        ),
    ]
