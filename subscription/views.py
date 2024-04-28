from typing import Any

from .models import Subscription


class SubscriptionManager:
    def __init__(self, user: Any) -> None:
        self.user = user

    def update_subscriptions(self, selected_categories: Any, user: Any) -> None:

        user_subscriptions = Subscription.objects.filter(user=user)

        if not user_subscriptions.exists():
            Subscription.objects.create(user=self.user)
            user_subscriptions = Subscription.objects.filter(user=self.user)

        user_subscriptions.first().categories.set(selected_categories)
