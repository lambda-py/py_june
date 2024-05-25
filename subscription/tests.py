from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from categories.models import Category, MainCategory
from core.tests import TestDataMixin
from posts.models import Post
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


class PostsOfSubscribedCategoriesViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_login(self.user)

        self.main_category1 = MainCategory.objects.create(title="Main Category 1")
        self.main_category2 = MainCategory.objects.create(title="Main Category 2")

        self.category1 = Category.objects.create(
            title="Category 1", main_category=self.main_category1
        )
        self.category2 = Category.objects.create(
            title="Category 2", main_category=self.main_category2
        )
        self.category3 = Category.objects.create(
            title="Category 3", main_category=self.main_category2
        )

        self.subscription = Subscription.objects.create(user=self.user)
        self.subscription.categories.add(self.category1)
        self.subscription.categories.add(self.category2)

        self.post1 = Post.objects.create(
            title="Post 1",
            content="Content 1",
            category=self.category1,
            author=self.user,
        )
        self.post2 = Post.objects.create(
            title="Post 2",
            content="Content 2",
            category=self.category2,
            author=self.user,
        )
        self.post3 = Post.objects.create(
            title="Post 3",
            content="Content 3",
            category=self.category3,
            author=self.user,
        )

    def test_get_posts_of_subscribed_categories(self):
        response = self.client.get(reverse("subscription:posts_of_subcribed"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "subscription/posts_of_subscribed_categories.html"
        )
        self.assertCountEqual(response.context["posts"], [self.post1, self.post2])
        self.assertQuerysetEqual(
            response.context["posts"], [self.post1, self.post2], ordered=False
        )
