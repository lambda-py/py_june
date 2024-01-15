from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from posts.models import Post

from .forms import AnswerCommentForm, CommentForm
from .models import Comment


class CreateCommentView(LoginRequiredMixin, View):
    template_name = "comments/comment_form.html"
    login_url = "/users/login/"

    def get(self, request: HttpRequest, post_slug: str) -> HttpResponse:
        post = get_object_or_404(Post, slug=post_slug)
        form = CommentForm()
        return render(request, self.template_name, {"form": form, "post": post})

    def post(self, request: HttpRequest, post_slug: str) -> HttpResponse:
        form = CommentForm(request.POST)
        post = get_object_or_404(Post, slug=post_slug)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = self.request.user
            comment.post_id = post.pk
            comment.save()
            return redirect("categories:detail", category_slug=post.category.slug)

        return render(request, self.template_name, {"form": form, "post": post})


class UpdateCommentView(UserPassesTestMixin, View):
    template_name = "comments/comment_update.html"

    def test_func(self) -> bool:
        comment_pk = self.kwargs.get("comment_pk")
        comment = get_object_or_404(Comment, pk=comment_pk)
        return comment.author == self.request.user

    def get(
        self, request: HttpRequest, post_slug: str, comment_pk: int
    ) -> HttpResponse:
        post = get_object_or_404(Post, slug=post_slug)
        comment = get_object_or_404(Comment, pk=comment_pk)
        form = CommentForm(instance=comment)
        return render(
            request,
            self.template_name,
            {"form": form, "post": post, "comment": comment},
        )

    def post(
        self, request: HttpRequest, post_slug: str, comment_pk: int
    ) -> HttpResponse:
        form = CommentForm(request.POST)
        post = get_object_or_404(Post, slug=post_slug)
        comment = get_object_or_404(Comment, pk=comment_pk)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = self.request.user
            comment.post_id = post.pk
            comment.save()
            return redirect("posts:details", post_slug=post.slug)

        return render(
            request,
            self.template_name,
            {"form": form, "post": post, "comment": comment},
        )


class DeleteCommentView(UserPassesTestMixin, View):
    template_name = "comments/comment_delete.html"

    def test_func(self) -> bool:
        comment_pk = self.kwargs.get("comment_pk")
        comment = get_object_or_404(Comment, pk=comment_pk)
        return comment.author == self.request.user

    def get(
        self, request: HttpRequest, post_slug: str, comment_pk: int
    ) -> HttpResponse:
        post = get_object_or_404(Post, slug=post_slug)
        comment = get_object_or_404(Comment, pk=comment_pk)
        return render(request, self.template_name, {"post": post, "comment": comment})

    def post(
        self, request: HttpRequest, post_slug: str, comment_pk: int
    ) -> HttpResponse:
        comment = get_object_or_404(Comment, pk=comment_pk)
        post = get_object_or_404(Post, slug=post_slug)

        comment.delete()

        return redirect("posts:details", post_slug=post.slug)


class AnswerCommentView(LoginRequiredMixin, View):
    template_name = "comments/comment_answer.html"
    login_url = "/users/login/"

    def get(
        self, request: HttpRequest, post_slug: str, comment_pk: int
    ) -> HttpResponse:
        post = get_object_or_404(Post, slug=post_slug)
        comment = get_object_or_404(Comment, pk=comment_pk)
        form = AnswerCommentForm()

        return render(
            request,
            self.template_name,
            {"form": form, "post": post, "comment": comment},
        )

    def post(
        self, request: HttpRequest, post_slug: str, comment_pk: int
    ) -> HttpResponse:
        post = get_object_or_404(Post, slug=post_slug)
        form = AnswerCommentForm(request.POST)
        comment = get_object_or_404(Comment, pk=comment_pk)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = self.request.user
            answer.post_id = post.pk
            answer.save()
            return redirect("posts:details", post_slug=post.slug)

        return render(
            request,
            self.template_name,
            {"form": form, "post": post, "comment": comment},
        )
