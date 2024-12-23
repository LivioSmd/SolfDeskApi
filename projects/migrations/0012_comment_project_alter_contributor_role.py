# Generated by Django 5.1.3 on 2024-11-25 20:30

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0011_alter_contributor_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="project",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="projects.project",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="contributor",
            name="role",
            field=models.CharField(default="Dev", max_length=255),
        ),
    ]
