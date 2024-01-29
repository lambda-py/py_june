from django.test import TestCase
from django.urls import reverse

from comments.models import Comment
from core.tests import TestDataMixin
from posts.models import Post


class PostModelTest(TestDataMixin, TestCase):
    def test_post_model(self):
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.content, "Test content")
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.category, self.category)
        self.assertEqual(self.post.slug, "test-post")
        self.assertTrue(self.post.is_active)

    def test_post_model_str(self):
        self.assertEqual(str(self.post), "Test Post")

    def test_post_model_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), "/posts/test-post/")


class CreatePostViewTest(TestDataMixin, TestCase):
    def setUp(self):
        super().setUp()
        Post.objects.all().delete()
        self.create_view_url = reverse(
            "posts:create", kwargs={"category_slug": self.category.slug}
        )

    def test_create_post_view_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.create_view_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/post_form.html")

    def test_create_post_view_post(self):
        self.client.force_login(self.user)

        data = {
            "title": "test title",
            "content": "Test text",
        }

        response = self.client.post(self.create_view_url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/posts/test-title/")
        self.assertEqual(self.category.posts.count(), 1)

    def test_create_post_view_post_invalid_data(self):
        self.client.force_login(self.user)

        data = {}

        response = self.client.post(self.create_view_url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/post_form.html")
        self.assertEqual(self.category.posts.count(), 0)


class DetailsPostViewTest(TestDataMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.detail_post_view_url = reverse(
            "posts:details", kwargs={"post_slug": self.post.slug}
        )

    def test_detail_post_view(self):
        response = self.client.get(self.detail_post_view_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/post_detail.html")
        self.assertEqual(response.context["post"], self.post)

    def test_detail_post_view_404(self):
        self.post.is_active = False
        self.post.save()

        response = self.client.get(self.detail_post_view_url)

        self.assertEqual(response.status_code, 404)

    def test_detail_post_view_empty_comment(self):
        self.client.force_login(self.user)
        data = {
            "content": "",
        }

        response = self.client.post(self.detail_post_view_url, data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("error_message", response.context)

    def test_detail_post_view_reply_post(self):
        self.client.force_login(self.user)
        Comment.objects.all().delete()
        data = {
            "content": "New content",
        }

        response = self.client.post(self.detail_post_view_url, data)
        self.assertEqual(self.post.comments.count(), 1)
        self.assertEqual(response.status_code, 302)


class UpdatePostViewTest(TestDataMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.update_post_view_url = reverse(
            "posts:update", kwargs={"post_slug": self.post.slug}
        )

    def test_update_post_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.update_post_view_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/post_update.html")

    def test_update_post_post(self):
        self.client.force_login(self.user)

        data = {
            "title": "Update title",
            "content": "Update content",
        }

        response = self.client.post(self.update_post_view_url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("posts:details", kwargs={"post_slug": self.post.slug})
        )
        update_post = Post.objects.get(pk=self.post.pk)
        self.assertEqual(update_post.title, "Update title")
        self.assertEqual(update_post.content, "Update content")


class DeletePostViewTest(TestDataMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.delete_post_view_url = reverse(
            "posts:delete", kwargs={"post_slug": self.post.slug}
        )

    def test_delete_post_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.delete_post_view_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/post_delete.html")

    def test_delete_post_post(self):
        self.client.force_login(self.user)

        response = self.client.post(self.delete_post_view_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("categories:list"))

        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
