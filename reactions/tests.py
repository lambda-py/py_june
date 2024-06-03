from django.test import TestCase
from django.urls import reverse

from core.tests import TestDataMixin


class ReactionsPostViewTest(TestDataMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.reactions_url = reverse("reactions:like_post", kwargs={"id": self.post.id})

    def test_reaction_model(self):
        self.assertEqual(self.reaction.user_id, self.user.id)
        self.assertEqual(self.reaction.post_id, self.post.pk)

    def test_reaction_post(self):
        self.client.force_login(self.user)
        response = self.client.post(self.reactions_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.reaction.user_id, self.user.id)
        self.assertEqual(self.reaction.post_id, self.post.pk)
