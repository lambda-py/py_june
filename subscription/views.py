from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView, View

from categories.models import Category, MainCategory
from posts.models import Post

from .forms import SubscriptionForm
from .models import Subscription


class SubscriptionCreateView(CreateView):
    model = Subscription
    form_class = SubscriptionForm

    def __init__(self, user: Any) -> None:
        super().__init__()
        self.user = user

    def update_subscriptions(self, selected_categories: Any, user: Any) -> None:
        user_subscriptions = Subscription.objects.filter(user=user)

        if not user_subscriptions.exists():
            Subscription.objects.create(user=self.user)
            user_subscriptions = Subscription.objects.filter(user=self.user)

        user_subscriptions.first().categories.set(selected_categories)


class PostsOfSubscribedCategoriesView(LoginRequiredMixin, View):
    template_name = "subscription/posts_of_subscribed_categories.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: dict) -> HttpResponse:
        user = request.user
        subscribed_categories = user.subscriptions.categories.all()
        posts = Post.objects.filter(
            category__in=subscribed_categories,
            is_active=True,
        ).order_by("-created_at")

        categories = Category.objects.annotate().select_related("main_category")

        main_categories = MainCategory.objects.all()

        context = {
            "main_categories": main_categories,
            "posts": posts,
            "subscribed_categories": subscribed_categories,
            "categories": categories,
        }

        return render(
            request,
            "subscription/posts_of_subscribed_categories.html",
            context,
        )
