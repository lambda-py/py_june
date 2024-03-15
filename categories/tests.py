from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from categories.models import Category, MainCategory
from core.tests import TestDataMixin
from posts.models import Post


class CategoryModelTest(TestCase):
    def setUp(self):
        self.main_category = MainCategory.objects.create(title="MainCategory")
        self.category = Category(
            title="Українська категорія",
            description="Test description",
            main_category=self.main_category,
        )
        # It is required to create slug
        self.category.save()

    def test_category_model(self):
        self.assertEqual(self.category.title, "Українська категорія")
        self.assertEqual(self.category.slug, "ukrayinska-kategoriia")
        self.assertEqual(self.category.description, "Test description")
        self.assertEqual(self.category.main_category.title, "MainCategory")

    def test_category_model_str(self):
        self.assertEqual(str(self.category), "Українська категорія")


class CategoryListViewTest(TestCase):
    def setUp(self):
        # Create some MainCategory instances for testing
        self.category1 = MainCategory.objects.create(title="Category 1")
        self.category2 = MainCategory.objects.create(title="Category 2")

    def test_category_list(self):
        response = self.client.get(reverse("categories:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Category 1")


class CategoryDetailViewTest(TestDataMixin, TestCase):
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
        for i in range(15):
            Post.objects.create(
                title=f"Test Post {i}",
                slug=f"test-post-{i}",
                content=f"Test content{i}",
                author=self.user,
                category=self.category,
            )

    def test_category_detail(self):
        response = self.client.get(
            reverse("categories:detail", kwargs={"category_slug": self.category.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post 1")

        self.assertEqual(len(response.context["page_obj"]), 10)
        self.assertContains(response, f'href="?page=2"')

        response_page_2 = self.client.get(
            reverse("categories:detail", kwargs={"category_slug": self.category.slug})
            + "?page=2"
        )
        self.assertEqual(response_page_2.status_code, 200)
        self.assertEqual(len(response_page_2.context["page_obj"]), 5)

        redirect_to_profile = self.client.get(
            reverse("profile:profile", kwargs={"profile": self.user.username})
        )
        self.assertEqual(redirect_to_profile.status_code, 302)
