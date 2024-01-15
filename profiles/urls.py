from django.urls import path

from .views import ProfiletView

app_name = "profile"

urlpatterns = [
    path("<slug:profile>/", ProfiletView.as_view(), name="profile"),
]
