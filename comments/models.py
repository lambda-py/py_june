from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


class Comment(models.Model):
    content = RichTextUploadingField(max_length=500, blank=True)
    author = models.ForeignKey(
        "users.ForumUser", on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(
        "posts.Post", on_delete=models.CASCADE, related_name="comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "comments"
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title