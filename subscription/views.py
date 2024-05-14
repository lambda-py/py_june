from typing import Any

from django.views.generic import CreateView

from .forms import SubscriptionForm
from .models import Subscription


class SubscriptionCreateView(CreateView):
    model = Subscription
    form_class = SubscriptionForm

    def __init__(self, user: Any) -> None:
        super().__init__()
        self.user = user

    def update_subscriptions(self, selected_categories: Any, user: Any) -> None:
        user_subscriptions = Subscription.objects.filter(user=user)

        if not user_subscriptions.exists():
            Subscription.objects.create(user=self.user)
            user_subscriptions = Subscription.objects.filter(user=self.user)

        user_subscriptions.first().categories.set(selected_categories)
