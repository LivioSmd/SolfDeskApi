# Generated by Django 5.1.3 on 2024-11-16 20:18

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0003_contributor"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="contributor",
        ),
    ]
