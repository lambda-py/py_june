from django.test import TestCase
from django.urls import reverse

from comments.forms import CommentForm
from comments.models import Comment
from core.tests import TestDataMixin


class CreateCommentTest(TestDataMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.create_comment_url = reverse(
            "comments:create", kwargs={"post_slug": self.post.slug}
        )

    def test_create_comment_view_get(self):
        self.client.force_login(self.user)

        response = self.client.get(self.create_comment_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "comments/comment_form.html")
        self.assertIsInstance(response.context["form"], CommentForm)
        self.assertEqual(response.context["post"], self.post)

    def test_create_comment_view_post(self):
        self.client.force_login(self.user)

        data = {
            "content": "Rest comment content1",
        }

        response = self.client.post(self.create_comment_url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse(
                "categories:detail", kwargs={"category_slug": self.post.category.slug}
            ),
        )

        comment = Comment.objects.get(content="Rest comment content1")
        self.assertEqual(comment.post, self.post)


class UpdateCommentTest(TestDataMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.update_comment_url = reverse(
            "comments:update",
            kwargs={"post_slug": self.post.slug, "comment_pk": self.comment.pk},
        )

    def test_update_comment_view_get(self):
        self.client.force_login(self.user)

        response = self.client.get(self.update_comment_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "comments/comment_update.html")
        self.assertIsInstance(response.context["form"], CommentForm)
        self.assertEqual(response.context["post"], self.post)

    def test_update_comment_view_post(self):
        self.client.force_login(self.user)

        data = {
            "content": "Update comment content1",
        }

        response = self.client.post(self.update_comment_url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("posts:details", kwargs={"post_slug": self.post.slug})
        )

        comment = Comment.objects.get(content="Update comment content1")
        self.assertEqual(comment.content, "Update comment content1")
        self.assertEqual(comment.post, self.post)


class DeleteCommentTest(TestDataMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.delete_comment_url = reverse(
            "comments:delete",
            kwargs={"post_slug": self.post.slug, "comment_pk": self.comment.pk},
        )

    def test_delete_comment_view_get(self):
        self.client.force_login(self.user)

        response = self.client.get(self.delete_comment_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "comments/comment_delete.html")

    def test_delete_comment_view_post(self):
        self.client.force_login(self.user)

        response = self.client.post(self.delete_comment_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("posts:details", kwargs={"post_slug": self.post.slug})
        )
