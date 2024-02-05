from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.middleware.csrf import get_token
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import DeleteView

from categories.models import Category
from comments.forms import CommentForm
from comments.models import Comment
from posts.forms import PostForm
from posts.models import Post


def can_user_post(request: HttpRequest) -> bool:
    user = request.user
    if last_post_time := user.last_post_time:
        time_diff = timezone.now() - last_post_time
        time_out = settings.POST_TIME_OUT
        if time_diff.total_seconds() < time_out:
            return False
    return True


class CreatePostView(LoginRequiredMixin, View):
    template_name = "posts/post_form.html"

    def get(self, request: HttpRequest, category_slug: str) -> HttpResponse:
        if can_user_post(request):
            category = get_object_or_404(Category, slug=category_slug)
            form = PostForm()
            return render(
                request, self.template_name, {"form": form, "category": category}
            )
        else:
            message = _("You can only post every 5 minutes.")
            return HttpResponseForbidden(message)

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
            return redirect(post.get_absolute_url())

        return render(request, self.template_name, {"form": form, "category": category})


class DetailsPostView(View):
    template_name = "posts/post_detail.html"

    def get(self, request: HttpRequest, post_slug: str) -> HttpResponse:
        post = get_object_or_404(Post, slug=post_slug, is_active=True)
        comments = Comment.objects.filter(post_id=post.id).order_by("-updated_at")
        post_comment_form = CommentForm(content_id=1)  # type: ignore[arg-type]
        reply_comment_form = CommentForm(content_id=2)  # type: ignore[arg-type]

        paginator = Paginator(comments, settings.COMMENTS_PAGINATION_PER_PAGE)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            self.template_name,
            {
                "post": post,
                "post_comment_form": post_comment_form,
                "reply_comment_form": reply_comment_form,
                "page_obj": page_obj,
            },
        )

    def post(self, request: HttpRequest, post_slug: str) -> HttpResponse:
        post = get_object_or_404(Post, slug=post_slug, is_active=True)
        form = CommentForm(request.POST)
        comments = Comment.objects.filter(post_id=post.id).order_by("-updated_at")
        post_comment_form = CommentForm(content_id=1)  # type: ignore[arg-type]
        reply_comment_form = CommentForm(content_id=2)  # type: ignore[arg-type]

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = self.request.user
            comment.post = post
            comment.save()

            return redirect(post.get_absolute_url())

        error_message = "An empty comment cannot be created"

        paginator = Paginator(comments, settings.COMMENTS_PAGINATION_PER_PAGE)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            self.template_name,
            {
                "post_comment_form": post_comment_form,
                "reply_comment_form": reply_comment_form,
                "post": post,
                "error_message": error_message,
                "page_obj": page_obj,
            },
        )


class UpdatePostView(View):
    template_name = "posts/post_update.html"

    def test_func(self, post) -> bool:
        return post.author == self.request.user

    def get(self, request: HttpRequest, post_slug: str) -> JsonResponse:
        post = get_object_or_404(Post, slug=post_slug)
        if not self.test_func(post):
            raise PermissionDenied()
        form = PostForm(instance=post)
        form_html = render_to_string("posts/post_update.html", {"form": form, "post": post})
        return JsonResponse({"form_html": form_html})

    def post(self, request: HttpRequest, post_slug: str) -> JsonResponse:
        post = get_object_or_404(Post, slug=post_slug)
        if not self.test_func(post):
            raise PermissionDenied()

        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return JsonResponse({"success": True})

        else:
            return JsonResponse({"success": False}, status=400)


class DeletePostView(View):
    template_name = "posts/post_delete.html"

    def test_func(self, post) -> bool:
        return post.author == self.request.user

    def get(self, request: HttpRequest, post_slug: str) -> JsonResponse:
        post = get_object_or_404(Post, slug=post_slug)
        if not self.test_func(post):
            raise PermissionDenied()
        delete_html = render_to_string("posts/post_delete.html", {"post": post})
        return JsonResponse({"delete_html": delete_html})

    def post(self, request: HttpRequest, post_slug: str) -> JsonResponse:
        post = get_object_or_404(Post, slug=post_slug)
        if not self.test_func(post):
            raise PermissionDenied()

        post.delete()
        return JsonResponse({"success": True})
