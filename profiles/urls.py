from django.urls import path

from .views import EditProfileView, ProfileView

app_name = "profile"

urlpatterns = [
    path("<slug:profile>/", ProfileView.as_view(), name="profile"),
    path(
        "<slug:profile>/edit-profile/", EditProfileView.as_view(), name="edit-profile"
    ),
]
