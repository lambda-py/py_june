from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static
from django_resized import ResizedImageField


class ForumUser(AbstractUser):
    bio = RichTextUploadingField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    last_post_time = models.DateTimeField(null=True, blank=True)
    avatar = ResizedImageField(
        size=[256, 256], null=True, blank=True, upload_to="uploads/profiles/avatars/"
    )

    def get_avatar_url(self) -> str:
        """
        Go through all social accounts and get first avatar url
        or return default avatar
        :return: url to user avatar
        """

        if self.avatar:
            return self.avatar.url
        else:
            for social_account in self.socialaccount_set.all():
                if social_account.provider == "github":
                    return social_account.extra_data.get("avatar_url")

            return static("images/default_avatar.png")
