# Generated by Django 4.2.4 on 2023-08-20 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0039_facettebehaviour_criticality"),
    ]

    operations = [
        migrations.CreateModel(
            name="ResultShareWidget",
            fields=[
                (
                    "widget_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="web.widget",
                    ),
                ),
            ],
            bases=("web.widget",),
        ),
    ]