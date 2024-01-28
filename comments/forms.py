from django import forms
from django.utils.translation import gettext_lazy as _

from core.ckeditor.widgets import DarkCKEditorWidget
from core.utils.html_sanitizer import html_sanitizer

from .models import Comment


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=DarkCKEditorWidget())

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        content_id = kwargs.pop("content_id", None)
        super().__init__(*args, **kwargs)
        # Change id of the widget to avoid conflicts with other widgets on the page
        # Use them in the template to iterate over them
        # Example:
        #         post_comment_form = CommentForm(content_id=1)
        #         reply_comment_form = CommentForm(content_id=2)
        # Perhaps there is a better way to do this
        if content_id:
            self.fields["content"].widget = DarkCKEditorWidget(attrs={"id": content_id})

    class Meta:
        model = Comment
        fields = ["content"]
        labels = {"content": _("Comment")}

    def clean_content(self) -> str:
        content = self.cleaned_data.get("content")
        return html_sanitizer(content)
