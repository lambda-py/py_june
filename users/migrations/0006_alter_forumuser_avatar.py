# Generated by Django 5.0.3 on 2024-03-25 08:15

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_forumuser_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="forumuser",
            name="avatar",
            field=django_resized.forms.ResizedImageField(
                blank=True,
                crop=None,
                force_format=None,
                keep_meta=True,
                null=True,
                quality=-1,
                scale=None,
                size=[256, 256],
                upload_to="uploads/profiles/avatars/",
            ),
        ),
    ]