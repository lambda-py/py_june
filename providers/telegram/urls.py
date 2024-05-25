from django.urls import path, include
from .views import TelegramOAuth2Adapter
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

urlpatterns = [
    path('accounts/', include('allauth.urls')),
]

urlpatterns += default_urlpatterns(TelegramOAuth2Adapter)
