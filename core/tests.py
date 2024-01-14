from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from categories.models import Category, MainCategory
from comments.models import Comment
from posts.models import Post


class TestDataMixin:
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
        )
        self.main_category = MainCategory.objects.create(title="MainCategory")
        self.category = Category.objects.create(
            title="Test category",
            slug="test-category",
            description="Test description",
            main_category=self.main_category,
        )

        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="Test content",
            author=self.user,
            category=self.category,
        )

        self.comment = Comment.objects.create(
            content="Test Comment content",
            author=self.user,
            post_id=self.post.pk,
        )


class HomePageTest(TestDataMixin, TestCase):
    def test_home_page_get_success(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

        self.assertIn(self.post, response.context["last_posts"])
        self.assertIn(self.post, response.context["most_hot"])
        self.assertIn(self.comment, response.context["user_activities"])
