from base64 import b64encode
from random import choice
from string import ascii_letters, digits

from httpx import Client

from services.abstract_auth_service import AbstractAuthService
from settings import settings


class YandexAuthService(AbstractAuthService):
    def __init__(self):
        self.client_id = settings.YANDEX_AUTH_CLIENT_ID
        self.client_secret = settings.YANDEX_AUTH_CLIENT_SECRET
        self.callback_url = settings.YANDEX_CALLBACK_URL

        self.user_data = {}

    def get_auth_link(self):
        """выдача ссылки для авторизации в аккаунте социальной сети.
        """

        authorize_url = settings.YANDEX_OAUTH_URL + '/authorize'
                
        symbols = ascii_letters + digits
        rand_string = ''.join(choice(symbols) for i in range(8))

        scope = 'login:email login:info'
        url = authorize_url + '?response_type=code&client_id={client_id}&redirect_uri={callback_url}&scope={scope}'\
            '&state={state}&display=popup'.format(
                client_id=self.client_id, 
                callback_url=self.callback_url, 
                state=rand_string, 
                scope=scope
            )

        return url

    def get_token(self, code: str):
        """Получение токена авторизации по коду авторизации.
        """

        token_url = settings.YANDEX_OAUTH_URL + '/token'
            
        data = {
            'grant_type': 'authorization_code',
            'code': code
        }

        str = self.client_id + ':' + self.client_secret

        b_str = str.encode('ASCII')
        encoded_str = b64encode(b_str)

        headers = {'Authorization': 'Basic ' + encoded_str.decode('ASCII')}
        client = Client()
        res = client.post(token_url, headers=headers, data=data)

        return res.json()

    def get_profile(self, token: str):
        """Получение email пользователя 
        """

        url = 'https://login.yandex.ru/info?format=json'
            
        headers = {'Authorization': 'OAuth ' + token}

        client = Client()
        res = client.get(url, headers=headers)
        
        json_res = res.json()

        self.user_data['email'] = json_res['default_email']

        return res.json()
