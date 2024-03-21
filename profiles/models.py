from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(
        "users.ForumUser", on_delete=models.CASCADE, related_name="profile"
    )
    github_link = models.CharField(max_length=100, blank=True)
    linkedin_link = models.CharField(max_length=100, blank=True)
    instagram_link = models.CharField(max_length=100, blank=True)
