from django.test import TestCase
from django.urls import reverse

from core.tests import TestDataMixin


class ReactionsPostViewTest(TestDataMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.reactions_url = reverse("reactions:like_post", kwargs={"id": self.post.id})
        self.detail_post_view_url = reverse(
            "posts:details", kwargs={"post_slug": self.post.slug}
        )

    def test_reaction_model(self):
        self.assertEqual(self.reaction.user_id, self.user.id)
        self.assertEqual(self.reaction.post_id, self.post.pk)

    def test_reaction_redirection(self):
        self.client.force_login(self.user)
        response = self.client.get(self.reactions_url)
        self.assertEqual(response.status_code, 302)
        redirected_url = response.url
        expected_url = reverse("posts:details", kwargs={"post_slug": self.post.slug})
        self.assertEqual(redirected_url, expected_url)

    def test_reaction_exist(self):
        self.client.force_login(self.user)
        response = self.client.post(self.reactions_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.reaction.user_id, self.user.id)
        self.assertEqual(self.reaction.post_id, self.post.pk)
