from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms
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

    def github(self) -> str:
        github = self.cleaned_data.get("github_link")

        if github == "":
            return ""
        elif github.startswith("https://github.com/"):
            return github
        else:
            return "Error"

    def linkedin(self) -> str:
        linkedin = self.cleaned_data.get("linkedin_link")

        if linkedin == "":
            return ""
        elif linkedin.startswith("https://www.linkedin.com/in/"):
            return linkedin
        else:
            return "Error"

    def instagram(self) -> str:
        instagram = self.cleaned_data.get("instagram_link")

        if instagram == "":
            return ""
        elif instagram.startswith("https://www.instagram.com/"):
            return instagram
        else:
            return "Error"
