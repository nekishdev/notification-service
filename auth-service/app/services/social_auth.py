from random import choice
from string import ascii_letters, digits

from werkzeug.security import generate_password_hash

from helpers.db import db
from helpers.http import failed
from helpers.jwt import refresh_tokens
from models.models import User, UserLoginRecord
from services.abstract_auth_service import AbstractAuthService
from services.vk_auth_service import VKAuthService
from services.yandex_auth_service import YandexAuthService


def auth_service_by_name(service_name: str) -> AbstractAuthService:
    if service_name == 'yandex':
        return YandexAuthService()
    elif service_name == 'vk':
        return VKAuthService()


def process_auth_token(auth_service_name: str, code: str, user_agent: str):
    auth_service: AbstractAuthService = auth_service_by_name(auth_service_name)

    if auth_service is None:
        return failed(message='Unknown authorization service name')

    token_info = auth_service.get_token(code)

    access_token = token_info['access_token']

    if token_info.get('email'):
        auth_service.user_data['email'] = token_info['email']

    auth_service.get_profile(access_token)

    login = auth_service.user_data['email']
    user = User.query.filter_by(login=login).first()

    return_data = {}
    if user is None:
        symbols = ascii_letters + digits
        password = ''.join(choice(symbols) for i in range(12))
        user = User(login=login, password=generate_password_hash(password))
        db.session.add(user)
        return_data['generated_password'] = password

    roles = [role.name for role in user.roles]

    access_token, refresh_token = refresh_tokens(login, user.id, roles)

    return_data['access_token'] = access_token
    return_data['refresh_token'] = refresh_token

    login_record = UserLoginRecord(user_agent=user_agent,
                                   access_token=access_token,
                                   refresh_token=refresh_token)
    user.login_records.append(login_record)

    db.session.commit()

    return return_data
