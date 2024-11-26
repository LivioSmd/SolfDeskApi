# Generated by Django 5.1.3 on 2024-11-19 22:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0010_alter_issue_assigned_user_alter_issue_author_comment"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="contributor",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contributors",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
