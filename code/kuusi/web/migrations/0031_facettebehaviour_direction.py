# Generated by Django 4.2.4 on 2023-08-19 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0030_facettebehaviour_subjects_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="facettebehaviour",
            name="direction",
            field=models.CharField(
                choices=[
                    ("SUBJECT_TO_OBJECT", "SUBJECT_TO_OBJECT"),
                    ("OBJECT_TO_SUBJECT", "OBJECT_TO_SUBJECT"),
                    ("BIDRECTIONAL", "BIDRECTIONAL"),
                ],
                default="BIDRECTIONAL",
                max_length=20,
            ),
        ),
    ]
