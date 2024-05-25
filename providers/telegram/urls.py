from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from django.urls import include, path

from .views import TelegramOAuth2Adapter

urlpatterns = [
    path("accounts/", include("allauth.urls")),
]

urlpatterns += default_urlpatterns(TelegramOAuth2Adapter)
