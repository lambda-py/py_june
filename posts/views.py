from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import BooleanField, Case, Count, IntegerField, When
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
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
from reactions.models import CommentsReactions, Reactions


def can_user_post(request: HttpRequest) -> bool:
    user = request.user
    if user.is_superuser:
        return True

    if last_post_time := user.last_post_time:
        time_diff = timezone.now() - last_post_time
        time_out = settings.POST_TIME_OUT
        if time_diff.total_seconds() < time_out:
            return False
    return True


class CreatePostView(LoginRequiredMixin, View):
    template_name = "posts/post_form.html"

    def get(self, request: HttpRequest, category_slug: str) -> HttpResponse:
        category = get_object_or_404(Category, slug=category_slug)
        if can_user_post(request):
            form = PostForm()
            return render(
                request, self.template_name, {"form": form, "category": category}
            )
        else:
            messages.success(request, _("You can only post every 5 minutes."))
            return redirect("categories:detail", category_slug=category.slug)

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
            messages.success(request, _("Post was created successfully"))
            return redirect(post.get_absolute_url())

        return render(request, self.template_name, {"form": form, "category": category})


class DetailsPostView(View):
    template_name = "posts/post_detail.html"

    def get(self, request: HttpRequest, post_slug: str) -> HttpResponse:
        post = get_object_or_404(Post, slug=post_slug, is_active=True)
        likes_count = Reactions.objects.filter(post_id=post.id).count()
        is_liked = Reactions.objects.filter(
            post_id=post.id, user_id=self.request.user.id
        )

        comments = (
            Comment.objects.filter(post_id=post.id)
            .order_by("-created_at")
            .annotate(
                comment_likes=Count("comments_reactions"),
                user_like=Count(
                    Case(
                        When(comments_reactions__user_id=self.request.user.id, then=1),
                        output_field=IntegerField(),
                    )
                ),
            )
        )

        comment_edit_form = CommentForm(content_id=5)  # type: ignore[arg-type]
        post_comment_form = CommentForm(content_id=1)  # type: ignore[arg-type]
        reply_comment_form = CommentForm(content_id=2)  # type: ignore[arg-type]
        edit_post_form = PostForm(content_id=3, instance=post)  # type: ignore[arg-type]
        delete_post_form = PostForm(content_id=4, instance=post)  # type: ignore[arg-type]

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
                "edit_post_form": edit_post_form,
                "delete_post_form": delete_post_form,
                "comment_edit_form": comment_edit_form,
                "page_obj": page_obj,
                "like": likes_count,
                "is_liked": is_liked,
            },
        )

    def post(self, request: HttpRequest, post_slug: str) -> HttpResponse:
        post = get_object_or_404(Post, slug=post_slug, is_active=True)
        post_form = PostForm(request.POST, instance=post)
        comment_form = CommentForm(request.POST)

        if post_form.is_valid():
            if "delete" in request.POST:
                post.delete()
                comments = Comment.objects.filter(post_id=post.id).order_by(
                    "-created_at"
                )
                comments.delete()
                messages.success(request, _("Post was deleted successfully"))
                return redirect("/forum/")
            else:
                edit_post = post_form.save(commit=False)
                edit_post.save()
                messages.success(request, _("Post was changed successfully"))
                return redirect(post.get_absolute_url())

        if comment_form.is_valid():
            if "edit-comment" in request.POST:
                comment_id = request.POST.get("comment-id", None)
                comment = get_object_or_404(Comment, id=comment_id)
                comment_edit_form = CommentForm(request.POST, instance=comment)
                edit_comment = comment_edit_form.save(commit=False)
                edit_comment.save()
                messages.success(request, _("Comment was changed successfully"))
                return redirect(post.get_absolute_url())

            comment = comment_form.save(commit=False)
            comment.author = self.request.user
            comment.post = post
            comment.save()
            messages.success(request, _("Comment was created successfully"))
            return redirect(post.get_absolute_url())

        if "delete-comment" in request.POST:
            comment_id = request.POST.get("comment-id", None)
            comment = get_object_or_404(Comment, id=comment_id)
            comment.delete()
            messages.success(request, _("Comment was deleted successfully"))
            return redirect(post.get_absolute_url())

        if not post_form.is_valid():
            messages.error(request, _("Something went wrong"))

        if not comment_form.is_valid():
            messages.error(request, _("Comment can't be empty"))

        return redirect(post.get_absolute_url())


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
            return redirect(post.get_absolute_url())

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
