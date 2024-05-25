from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class TelegramAccount(ProviderAccount):
    def to_str(self):
        dflt = super(TelegramAccount, self).to_str()
        return self.account.extra_data.get('username', dflt)


class TelegramProvider(OAuth2Provider):
    id = 'telegram'
    name = 'Telegram'
    account_class = TelegramAccount

    def extract_uid(self, data):
        return str(data['id'])

    def extract_common_fields(self, data):
        return dict(username=data.get('username'),
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name'))


provider_classes = [TelegramProvider]
