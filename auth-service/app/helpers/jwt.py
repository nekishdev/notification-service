import uuid

from flask_jwt_extended import (JWTManager, create_access_token,
                                create_refresh_token, get_jti)

jwt = JWTManager()


def refresh_tokens(login: str, user_id: uuid, roles: list) -> tuple:
    additional_claims = {'id': user_id}
    refresh_token = create_refresh_token(identity=login, additional_claims=additional_claims)
    r_jti = get_jti(refresh_token)
    additional_claims = {'id': user_id, 'r_jti': r_jti, 'roles': roles}
    access_token = create_access_token(identity=login, additional_claims=additional_claims)
    return access_token, refresh_token


def jwt_init_app(app):
    jwt.init_app(app)
