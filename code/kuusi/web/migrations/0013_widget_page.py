# Generated by Django 4.2.4 on 2023-08-19 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0012_widget_col_widget_row_widget_width"),
    ]

    operations = [
        migrations.AddField(
            model_name="widget",
            name="page",
            field=models.ForeignKey(
                default=12,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="widget_page",
                to="web.page",
            ),
            preserve_default=False,
        ),
    ]
