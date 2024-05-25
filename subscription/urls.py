from django.urls import path

from subscription.views import PostsOfSubscribedCategoriesView

app_name = "subscription"

urlpatterns = [
    path("posts-of-subcribed/", PostsOfSubscribedCategoriesView.as_view(), name="posts_of_subcribed"),
]