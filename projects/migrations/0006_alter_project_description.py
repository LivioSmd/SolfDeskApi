# Generated by Django 5.1.3 on 2024-11-16 21:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0005_project_description_project_type_alter_project_actif"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="description",
            field=models.CharField(max_length=255),
        ),
    ]
