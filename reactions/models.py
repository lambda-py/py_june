from django.db import models
from core.models import SlugModel


class Reactions(SlugModel):
    user = models.OneToOneField(
        to="users.ForumUser",
        on_delete=models.CASCADE,
        null=True,
    )
    post = models.ForeignKey(
        "posts.Post", on_delete=models.CASCADE, related_name="reactions"
    )