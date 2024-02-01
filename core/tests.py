from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from categories.models import Category, MainCategory
from comments.models import Comment
from core.utils.is_empty_comment import is_empty_comment
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

    def test_answer_question_url_not_commented_first(self):
        Post.objects.create(
            title="Test Post 2",
            slug="test-post-2",
            content="Test content",
            author=self.user,
            category=self.category,
        )
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["answer_question_url"], "/posts/test-post-2/")

    def test_answer_question_url_last_post(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["answer_question_url"], "/posts/test-post/")

    def test_answer_question_url_no_posts(self):
        Post.objects.all().delete()
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["answer_question_url"], "")


class TestIsEmptyComment(TestCase):
    def setUp(self):
        self.test_content1 = "<blockquote><blockquote><p>1</p></blockquote><p>1</p></blockquote><p>&nbsp;</p>"
        self.test_content2 = "<blockquote><blockquote><p>1</p></blockquote><p>1</p></blockquote><p>Hello</p>"
        self.test_content3 = "<p>Hello</p>"

    def test(self):
        self.assertEqual(is_empty_comment(self.test_content1), True)
        self.assertEqual(is_empty_comment(self.test_content2), False)
        self.assertEqual(is_empty_comment(self.test_content3), False)
