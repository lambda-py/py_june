from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from users.models import ForumUser

from .models import Profile


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


class EditProfileLinksForm(forms.ModelForm):
    github_link = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "GitHub", "class": "col s12 social_links"}
        ),
    )
    linkedin_link = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Linkedin", "class": "col s12 social_links"}
        ),
    )
    instagram_link = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Instagram", "class": "col s12 social_links"}
        ),
    )

    class Meta:
        model = Profile
        fields = ["github_link", "linkedin_link", "instagram_link"]

    def clean(self) -> dict:
        cleaned_data = super().clean()

        github = cleaned_data.get("github_link")
        linkedin = cleaned_data.get("linkedin_link")
        instagram = cleaned_data.get("instagram_link")

        if github and not github.startswith("https://github.com/"):
            self.add_error(
                "github_link",
                _("Invalid GitHub profile URL. Please use format: https://github.com/"),
            )

        if linkedin and not linkedin.startswith("https://www.linkedin.com/in/"):
            self.add_error(
                "linkedin_link",
                _(
                    "Invalid Linkedin profile URL. Please use format: https://www.linkedin.com/in/"
                ),
            )

        if instagram and not instagram.startswith("https://www.instagram.com/"):
            self.add_error(
                "instagram_link",
                _(
                    "Invalid Instagram profile URL. Please use format: https://www.instagram.com/"
                ),
            )

        return cleaned_data
