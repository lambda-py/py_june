from django.urls import path

from subscription.views import SubscriptionPostView

app_name = "subscription"

urlpatterns = [
    path(
        "posts/",
        SubscriptionPostView.as_view(),
        name="posts_list",
    ),
]
