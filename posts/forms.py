from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms

from core.utils.html_sanitizer import html_sanitizer
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        super(PostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "title",
            "content",
            Submit("submit", "Confirm", css_class="btn waves-effect waves-light"),
        )
        self.field_order = ["title", "content"]

    def clean_content(self):
        content = self.cleaned_data.get("content")
        return html_sanitizer(content)
