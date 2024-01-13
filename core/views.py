from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from comments.models import Comment
from posts.models import Post


def home(request: HttpRequest) -> HttpResponse:
    last_posts = Post.objects.filter(is_active=True).order_by("-created_at")[:5]
    most_hot = (
        Post.objects.filter(is_active=True)
        .annotate(comment_count=Count("comments", distinct=True))
        .order_by("-comment_count")[:5]
    )

    need_help_posts = (
        Post.objects.filter(category_id=1, is_active=True)
        .annotate(comment_count=Count("comments", distinct=True))
        .filter(comment_count=0)
        .order_by("-created_at")[:5]
    )

    user_activities = Comment.objects.filter(is_active=True).order_by("-created_at")[:5]

    return render(
        request,
        "home.html",
        {
            "last_posts": last_posts,
            "most_hot": most_hot,
            "need_help_posts": need_help_posts,
            "user_activities": user_activities,
        },
    )
