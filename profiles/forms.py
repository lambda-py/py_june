from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms

from users.models import ForumUser


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = ForumUser
        fields = ["first_name", "last_name", "bio", "birth_date"]

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("first_name", css_class="col s12"),
                Column("last_name", css_class="col s12"),
            ),
            Row(
                Column("bio", css_class="col s12"),
                Column("birth_date", css_class="col s12"),
            ),
            Submit(
                "submit",
                "Update profile",
                css_class="btn waves-effect waves-light submit-button",
            ),
        )
        self.field_order = ["first_name", "last_name", "bio", "birth_date"]


class EditAvatarProfileForm(forms.ModelForm):
    avatar = forms.ImageField()

    class Meta:
        model = ForumUser
        fields = ["avatar"]
