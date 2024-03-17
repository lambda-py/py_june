from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms
from PIL import Image

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
    avatar = forms.ImageField().required = False

    class Meta:
        model = ForumUser
        fields = ["avatar"]

    def save(self) -> None:
        super(EditAvatarProfileForm, self).save()

        x = self.cleaned_data.get("x")
        y = self.cleaned_data.get("y")
        w = self.cleaned_data.get("width")
        h = self.cleaned_data.get("height")

        with Image.open(self.avatar) as img:
            cropped_image = img.crop((x, y, w + x, h + y))
            resized_image = cropped_image.resize((256, 256), Image.ANTIALIAS)
            resized_image.save(self.avatar)
            return img
