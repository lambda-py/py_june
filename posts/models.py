from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from core.models import SlugModel


class Post(SlugModel):
    title = models.CharField(max_length=50)
    content = RichTextUploadingField(max_length=2000)
    author = models.ForeignKey(
        "users.ForumUser", on_delete=models.CASCADE, related_name="posts"
    )
    category = models.ForeignKey(
        "categories.Category", on_delete=models.CASCADE, related_name="posts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "posts"
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("posts:details", kwargs={"post_slug": self.slug})
