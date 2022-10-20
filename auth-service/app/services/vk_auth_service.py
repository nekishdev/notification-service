from random import choice
from string import ascii_letters, digits

from httpx import Client

from services.abstract_auth_service import AbstractAuthService
from settings import settings


class VKAuthService(AbstractAuthService):
    def __init__(self):
        self.client_id = settings.VK_AUTH_CLIENT_ID
        self.client_secret = settings.VK_AUTH_CLIENT_SECRET
        self.callback_url = settings.VK_CALLBACK_URL

        self.user_data = {}

    def get_auth_link(self):
        """выдача ссылки для авторизации в аккаунте социальной сети.
        """

        authorize_url = settings.VK_OAUTH_URL + '/authorize'        

        symbols = ascii_letters + digits
        rand_string = ''.join(choice(symbols) for i in range(8))

        scope = 'email'
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

        token_url = settings.VK_OAUTH_URL + '/access_token'

        url = token_url + '?client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect}&code={code}'.format(
            client_id=self.client_id, 
            client_secret=self.client_secret, 
            redirect=self.callback_url, 
            code=code
        )

        client = Client()
        res = client.get(url)
        
        json_res = res.json()

        self.user_data['email'] = json_res['email']

        return json_res

    def get_profile(self, token: str):
        """Получение основной информации о пользователя 
        """

        url = 'https://api.vk.com/method/users.get?fields={fields}&access_token={token}&v={version}'.format(
            fields = '',
            token = token,
            version = '5.131'
        )

        client = Client()
        res = client.get(url)

        return res.json() 
