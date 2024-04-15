from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from comments.models import Comment
from posts.models import Post

from .models import CommentsReactions, Reactions


class PostReactionsView(LoginRequiredMixin, View):
    template_name = "ui/post/post_like.html"

    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        post = get_object_or_404(Post, pk=id, is_active=True)
        likes_count = Reactions.objects.filter(post_id=post.id).count()
        is_liked = Reactions.objects.filter(
            post_id=post.id, user_id=self.request.user.id
        )
        context = {
            "like": likes_count,
            "is_liked": is_liked,
        }
        return render(
            request,
            self.template_name, context)

    def post(self, request: HttpRequest, id: int) -> HttpResponseRedirect:
        post = get_object_or_404(Post, pk=id, is_active=True)

        if self.request.user != post.author:
            if not Reactions.objects.filter(
                post_id=post.id, user_id=self.request.user.id
            ).exists():
                Reactions.objects.create(user_id=self.request.user.id, post_id=post.id)
            else:
                Reactions.objects.filter(
                    user_id=self.request.user.id, post_id=post.id
                ).delete()

        likes_count = Reactions.objects.filter(post_id=post.id).count()
        is_liked = Reactions.objects.filter(
            post_id=post.id, user_id=self.request.user.id
        )

        context = {
            "like": likes_count,
            "is_liked": is_liked,
            "post_id": id,
        }
        return render(
            request,
            self.template_name, context)


class CommentReactionsView(LoginRequiredMixin, View):
    template_name = "posts/post_detail.html"

    def get(self, request: HttpRequest, post_slug: str, id: int) -> HttpResponse:
        post = get_object_or_404(Post, slug=post_slug, is_active=True)
        return redirect("posts:details", post_slug=post.slug)

    def post(
        self, request: HttpRequest, post_slug: str, id: int
    ) -> HttpResponseRedirect:
        user_comment = get_object_or_404(Comment, pk=id, is_active=True)

        if self.request.user != user_comment.author:
            if not CommentsReactions.objects.filter(
                comment_id=user_comment.id, user_id=self.request.user.id
            ).exists():
                CommentsReactions.objects.create(
                    user_id=self.request.user.id, comment_id=user_comment.id
                )
            else:
                CommentsReactions.objects.filter(
                    user_id=self.request.user.id, comment_id=user_comment.id
                ).delete()
        return redirect("posts:details", post_slug=post_slug)
