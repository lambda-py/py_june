from django import forms
from django.utils.translation import gettext_lazy as _

from core.utils.html_sanitizer import html_sanitizer

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        labels = {"title": _("Title*"), "content": _("Content*")}

    def clean_content(self) -> str:
        content = self.cleaned_data.get("content")
        return html_sanitizer(content)
