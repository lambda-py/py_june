from django import forms
from django.utils.translation import gettext_lazy as _

from core.utils.html_sanitizer import html_sanitizer

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        labels = {"content": _("Comment")}

    def clean_content(self) -> str:
        content = self.cleaned_data.get("content")
        return html_sanitizer(content)
