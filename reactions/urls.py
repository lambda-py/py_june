from django.urls import path

from .views import ReactionsView

app_name = "reactions"

urlpatterns = [
    path("like/<int:id>", ReactionsView.as_view(), name="like_post"),
]
