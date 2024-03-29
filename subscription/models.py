from django.db import models

from categories.models import Category
from users.models import ForumUser


class Subscription(models.Model):
    user = models.OneToOneField(
        ForumUser,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        primary_key=True,
    )
    categories = models.ManyToManyField(
        Category,
        related_name='subscriptions',
        blank=True,
    )

    def __str__(self):
        return f"Subscription {self.user.username}"
