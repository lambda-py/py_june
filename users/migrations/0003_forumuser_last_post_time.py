# Generated by Django 5.0.1 on 2024-01-17 08:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_forumuser_bio"),
    ]

    operations = [
        migrations.AddField(
            model_name="forumuser",
            name="last_post_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
