from django.urls import path

from .views import ProfileView

app_name = "profile"

urlpatterns = [
    path("<slug:profile>/", ProfileView.as_view(), name="profile"),
]
