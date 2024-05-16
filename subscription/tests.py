from django.test import TestCase
from django.urls import reverse

from categories.models import Category, MainCategory
from core.tests import TestDataMixin
from subscription.forms import SubscriptionForm
from subscription.models import Subscription


class SubscriptionCreateViewTest(TestDataMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.main_category = MainCategory.objects.create(title="MainCategory")
        self.subscription_create_view_url = reverse(
            "profile:edit-profile", kwargs={"profile": self.user.username}
        )

    def test_subscription_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.subscription_create_view_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "subscription/subscription_form.html")
        self.assertIsInstance(response.context["subscription_form"], SubscriptionForm)

    def test_subscription_post(self):
        self.client.force_login(self.user)

        data = [
            Category(
                title="Category 1",
                description="Test description",
                main_category=self.main_category,
            ),
            Category(
                title="Category 2",
                description="Test description",
                main_category=self.main_category,
            ),
        ]

        response = self.client.post(self.subscription_create_view_url)

        Category.objects.bulk_create(data)
        updated_subscriptions = Subscription.objects.get(user=self.user)
        updated_subscriptions.categories.set(data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("profile:profile", kwargs={"profile": self.user})
        )

        self.assertEqual(updated_subscriptions.categories.count(), 2)
        self.assertIn(data[0], updated_subscriptions.categories.all())
        self.assertIn(data[1], updated_subscriptions.categories.all())
