from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import SlugModel


class Profile(SlugModel):
    title = models.CharField(max_length=50, blank=True)
    link = models.CharField(max_length=500, blank=True)
    user_id = models.OneToOneField(
        to="users.ForumUser",
        on_delete=models.CASCADE,
        related_name="profile",
        null=True,
    )
