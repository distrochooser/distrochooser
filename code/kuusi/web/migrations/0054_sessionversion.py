# Generated by Django 4.2.4 on 2023-08-21 09:45

from django.db import migrations, models
import django.db.models.deletion
import web.models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0053_rename_next_page_target_page_next_page"),
    ]

    operations = [
        migrations.CreateModel(
            name="SessionVersion",
            fields=[
                (
                    "translateable_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="web.translateable",
                    ),
                ),
                (
                    "version_name",
                    web.models.TranslateableField(
                        help_text="A comment for translators to identify this value",
                        max_length=120,
                    ),
                ),
            ],
            bases=("web.translateable",),
        ),
    ]
