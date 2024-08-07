# Generated by Django 4.2.4 on 2023-08-26 09:25

from django.db import migrations, models
import django.db.models.deletion
import web.models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0066_delete_choosablemeta"),
    ]

    operations = [
        migrations.CreateModel(
            name="ChoosableMeta",
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
                    "meta_type",
                    models.CharField(
                        choices=[("TEXT", "TEXT")], default="TEXT", max_length=20
                    ),
                ),
                (
                    "meta_title",
                    web.models.TranslateableField(
                        blank=True,
                        help_text="A comment for translators to identify this value",
                        max_length=120,
                        null=True,
                    ),
                ),
                (
                    "meta_name",
                    models.CharField(
                        choices=[("AGE", "AGE")], default="AGE", max_length=25
                    ),
                ),
                ("meta_value", models.CharField(default="A value", max_length=255)),
                (
                    "meta_choosable",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="choosablemeta_choosable",
                        to="web.choosable",
                    ),
                ),
            ],
            bases=("web.translateable",),
        ),
    ]
