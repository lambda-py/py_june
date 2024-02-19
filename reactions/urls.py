from django.urls import path

from .views import CommentReactionsView, PostReactionsView

app_name = "reactions"

urlpatterns = [
    path("like/<int:id>", PostReactionsView.as_view(), name="like_post"),
    path(
        "like-comment/<slug:post_slug>/<int:id>",
        CommentReactionsView.as_view(),
        name="like_comment",
    ),
]
