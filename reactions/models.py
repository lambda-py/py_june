from django.db import models


class Reactions(models.Model):
    user = models.ForeignKey(
        to="users.ForumUser",
        on_delete=models.CASCADE,
        null=True,
        related_name="reactions",
    )
    post = models.ForeignKey(
        "posts.Post", on_delete=models.CASCADE, related_name="reactions"
    )
