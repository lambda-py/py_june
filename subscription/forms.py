from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from categories.models import Category
from subscription.models import Subscription


class SubscriptionForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Subscription
        fields = ["categories"]

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        user = kwargs.pop("user", None)
        super(SubscriptionForm, self).__init__(*args, **kwargs)
        self.user = user

        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Update subscriptions"))
        self.field_order = ["categories"]
