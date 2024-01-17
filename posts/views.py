from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import DeleteView

from categories.models import Category
from comments.forms import CommentForm
from comments.models import Comment
from posts.forms import PostForm
from posts.models import Post


def check_post_time_limit(request: HttpRequest) -> bool:
    user = request.user
    if user.is_authenticated:
        last_post_time = user.last_post_time
        if last_post_time:
            time_diff = timezone.now() - last_post_time
            if time_diff.total_seconds() < 300:
                return True
    return False


class CreatePostView(LoginRequiredMixin, View):
    template_name = "posts/post_form.html"
    login_url = "/users/login/"

    def get(self, request: HttpRequest, category_slug: str) -> HttpResponse:
        if check_post_time_limit(request):
            return HttpResponseForbidden("You can only post every 5 minutes.")
        else:
            category = get_object_or_404(Category, slug=category_slug)
            form = PostForm()
            return render(
                request, self.template_name, {"form": form, "category": category}
            )

    def post(self, request: HttpRequest, category_slug: str) -> HttpResponse:
        form = PostForm(request.POST)
        category = get_object_or_404(Category, slug=category_slug)

        if form.is_valid():
            post = form.save(commit=False)
            user = self.request.user
            user.last_post_time = timezone.now()
            post.author = self.request.user
            post.category = category
            post.save()
            user.save()
            return redirect("categories:list")

        return render(request, self.template_name, {"form": form, "category": category})


class DetailsPostView(View):
    template_name = "posts/post_detail.html"

    def get(self, request: HttpRequest, post_slug: str) -> HttpResponse:
        post = get_object_or_404(Post, slug=post_slug, is_active=True)
        comments = Comment.objects.filter(post_id=post.id).order_by("-updated_at")
        form = CommentForm()

        return render(
            request,
            self.template_name,
            {
                "post": post,
                "form": form,
                "comments": comments,
            },
        )

    def post(self, request: HttpRequest, post_slug: str) -> HttpResponse:
        post = get_object_or_404(Post, slug=post_slug, is_active=True)
        form = CommentForm(request.POST)
        comments = Comment.objects.filter(post_id=post.id).order_by("-updated_at")

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = self.request.user
            comment.post = post
            comment.save()
            return redirect("posts:details", post_slug=post.slug)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "post": post,
                "comments": comments,
            },
        )


class UpdatePostView(UserPassesTestMixin, View):
    template_name = "posts/post_update.html"

    def test_func(self) -> bool:
        post_slug = self.kwargs.get("post_slug")
        post = get_object_or_404(Post, slug=post_slug)
        return post.author == self.request.user

    def get(self, request: HttpRequest, post_slug: str) -> HttpResponse:
        post = get_object_or_404(Post, slug=post_slug)
        form = PostForm(instance=post)
        return render(
            request,
            self.template_name,
            {"form": form, "post": post},
        )

    def post(self, request: HttpRequest, post_slug: str) -> HttpResponse:
        post = get_object_or_404(Post, slug=post_slug)
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect("posts:details", post_slug=post.slug)

        return render(
            request,
            self.template_name,
            {"form": form, "post": post},
        )


class DeletePostView(UserPassesTestMixin, DeleteView):
    model = Post
    slug_url_kwarg = "post_slug"
    template_name = "posts/post_delete.html"
    success_url = reverse_lazy("categories:list")

    def test_func(self) -> bool:
        return self.get_object().author == self.request.user
