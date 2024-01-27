import uuid

from ckeditor.widgets import CKEditorWidget
from django import forms
from django.utils.translation import gettext_lazy as _

from core.utils.html_sanitizer import html_sanitizer
from .models import Comment


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # change id of the widget to avoid conflicts with other widgets on the page
        self.fields['content'].widget = CKEditorWidget(attrs={'id': uuid.uuid4()})

    class Meta:
        model = Comment
        fields = ["content"]
        labels = {"content": _("Comment")}

    def clean_content(self) -> str:
        content = self.cleaned_data.get("content")
        return html_sanitizer(content)
