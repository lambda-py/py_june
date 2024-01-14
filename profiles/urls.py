from django.urls import path

from .views import CreateProfileView, ProfiletView
app_name = "profile"

urlpatterns = [
    path("create/", CreateProfileView.as_view(), name="create"),
    path("<slug:profile_slug>/", ProfiletView.as_view(), name='profile')
]