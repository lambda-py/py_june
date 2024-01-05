from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from categories.models import Category
from posts.forms import PostForm
from posts.models import Post


class CreatePostView(LoginRequiredMixin, View):
    template_name = "posts/post_form.html"
    login_url = "/users/login/"

    def get(self, request: HttpRequest, category_id: int) -> HttpResponse:
        category = Category.objects.get(pk=category_id)
        form = PostForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest, category_id: int) -> HttpResponse:
        form = PostForm(request.POST)
        category = Category.objects.get(pk=category_id)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = self.request.user
            post.category = category
            post.save()
            return redirect("categories:list")

        return render(request, self.template_name, {"form": form, "category": category})


class DetailsPostView(View):
    template_name = "posts/post_detail.html"

    def get(self, request: HttpRequest, post_id: int) -> HttpResponse:
        post = get_object_or_404(Post, pk=post_id, is_active=True)

        return render(request, self.template_name, {"post": post})


class UpdatePostView(UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]
    template_name = "posts/post_update.html"
    success_url = reverse_lazy("categories:list")

    def test_func(self) -> bool:
        return self.get_object().author == self.request.user
