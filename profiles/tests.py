# from django.test import TestCase
# from django.urls import reverse

# from core.tests import TestDataMixin
# from users.models import ForumUser


# class UpdateProfileViewTest(TestDataMixin, TestCase):
#     def setUp(self):
#         super().setUp()
#         self.update_profile_view_url = reverse(
#             "profile:edit-profile", kwargs={"profile": self.user.username}
#         )

#     def test_update_profile_get(self):
#         self.client.force_login(self.user)
#         response = self.client.get(self.update_profile_view_url)

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "profiles/edit_profile.html")

#     def test_update_profile_post(self):
#         self.client.force_login(self.user)

#         data = {
#             "first_name": "Name",
#             "last_name": "Surname",
#             "bio": "My bio",
#             "birth_date": "2024-03-12",
#         }

#         response = self.client.post(self.update_profile_view_url, data)

#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(
#             response,
#             reverse("profile:profile", kwargs={"profile": self.user.username}),
#         )
#         updated_profile = ForumUser.objects.get(username=self.user.username)
#         self.assertEqual(updated_profile.first_name, "Name")
#         self.assertEqual(updated_profile.last_name, "Surname")
#         self.assertEqual(updated_profile.bio, "My bio")
#         self.assertEqual(updated_profile.birth_date.strftime("%Y-%m-%d"), "2024-03-12")
