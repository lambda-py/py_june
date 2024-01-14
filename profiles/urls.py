from django.urls import path

from .views import CreateProfileView, ProfiletView

app_name = "profile"

urlpatterns = [
    path("<slug:profile>/update/", CreateProfileView.as_view(), name="update"),
    path("<slug:profile>/", ProfiletView.as_view(), name="profile"),
]
