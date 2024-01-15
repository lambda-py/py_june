from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "content",
            Submit("submit", "Confirm", css_class="btn waves-effect waves-light"),
        )
        self.field_order = ["content"]


class AnswerCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        super(AnswerCommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "content",
            Submit("submit", "Answer", css_class="btn waves-effect waves-light"),
        )
        self.field_order = ["content"]
