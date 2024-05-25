import requests
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from allauth.socialaccount.providers.telegram.provider import TelegramProvider


class TelegramOAuth2Adapter(OAuth2Adapter):
    provider_id = TelegramProvider.id
    access_token_url = "https://oauth.telegram.org/token"
    authorize_url = "https://oauth.telegram.org/auth"
    profile_url = "https://api.telegram.org/bot{token}/getMe"

    def complete_login(self, request, app, token, response):
        extra_data = response.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)

    def get_profile(self, token):
        url = self.profile_url.format(token=token)
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()

    def get_authorize_url(self, request, app):
        authorize_url = self.authorize_url
        bot_id = app.client_id
        origin = request.build_absolute_uri("/")
        return_to = request.build_absolute_uri("/accounts/telegram/login/callback/")
        return f"{authorize_url}?bot_id={bot_id}&origin={origin}&return_to={return_to}&request_access=write&embed=0"
