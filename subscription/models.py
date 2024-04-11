from django.db import models

from categories.models import Category
from users.models import ForumUser


class Subscription(models.Model):
    user = models.OneToOneField(
        ForumUser,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        primary_key=True,
    )
    categories = models.ManyToManyField(
        Category,
        related_name="subscriptions",
        blank=True,
    )

    class Meta:
        db_table = "subscriptions"
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        ordering = ["-user__username"]

    def __str__(self) -> str:
        return f"Subscription {self.user.username}"
