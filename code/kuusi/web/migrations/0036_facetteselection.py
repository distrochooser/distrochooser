# Generated by Django 4.2.4 on 2023-08-20 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0035_page_require_session"),
    ]

    operations = [
        migrations.CreateModel(
            name="FacetteSelection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "facette",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="facetteseletion_facette",
                        to="web.facette",
                    ),
                ),
            ],
        ),
    ]
