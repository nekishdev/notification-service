import uuid
from typing import Optional

from flask import Blueprint, request
from flask_jwt_extended import get_jwt, jwt_required
from sqlalchemy import desc
from werkzeug.security import check_password_hash, generate_password_hash

from helpers.db import db
from helpers.http import failed, success
from helpers.jwt import jwt, refresh_tokens
from helpers.redis import redis_conn
from models.models import User, UserLoginRecord
from settings import settings

user_router = Blueprint('user', __name__)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = redis_conn.get(jti)
    return token_in_redis is not None


@user_router.route('/register', methods=['POST'])
def register():
    """Register new user
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
           type: object
           properties:
             login:
               type: string
               example: Nikita
             password:
               type: string
               example: some-password-123
    responses:
      200:
        description: User created
    """
    login = request.json.get('login')
    password = request.json.get('password')

    if not login or not password:
        return failed('Request data malformed')

    user = User.query.filter_by(login=login).first()

    if user:
        return failed('User already exists')

    new_user = User(login=login, password=generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    return success('Successful registration')



@user_router.route('/login', methods=['POST'])
def login():
    """Login existent user
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
           type: object
           properties:
             login:
               type: string
               example: Nikita
             password:
               type: string
               example: some-password-123
    responses:
      200:
        description: User logged
    """
    login = request.json.get('login')

    user: Optional[User] = User.query.filter_by(login=login).first()

    if user is None:
        return failed('User {} doesn\'t exist'.format(login))

    password = request.json.get('password')
    if check_password_hash(user.password, password):
        roles = [role.name for role in user.roles]

        access_token, refresh_token = refresh_tokens(login, user.id, roles)

        login_record = UserLoginRecord(user_agent=request.headers.get('User-Agent'),
                                       access_token=access_token,
                                       refresh_token=refresh_token)
        user.login_records.append(login_record)

        db.session.commit()

        return success('User logged', {
            'access_token': access_token,
            'refresh_token': refresh_token,
        })
    else:
        return failed('Wrong password', 401)


@user_router.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    """Logout user
    ---
    security:
        - Bearer: []
    responses:
      200:
        description: Successful logout (tokens revoked)
    """
    jti = get_jwt()['jti']
    r_jti = get_jwt()['r_jti']
    try:
        redis_conn.set(jti, '', ex=settings.ACCESS_EXPIRES)
        redis_conn.set(r_jti, '', ex=settings.REFRESH_EXPIRES)
        return success('Access token revoked')
    except Exception as e:
        return failed('Error while revoking access token')


@user_router.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh pair of tokens
    ---
    security:
        - Bearer: []
    responses:
      200:
        description: Tokens refreshed
    """
    claims = get_jwt()
    login = claims['sub']

    user: Optional[User] = User.query.filter_by(login=login).first()

    if user is None:
        return failed('User {} doesn\'t exist'.format(login))

    roles = [role.name for role in user.roles]

    access_token, refresh_token = refresh_tokens(login, claims['id'], roles)

    return success('Token refreshed', {
        'access_token': access_token,
        'refresh_token': refresh_token
    })


@user_router.route('/login_history', methods=['POST'])
@jwt_required()
def login_history():
    """Login history
    ---
    security:
        - Bearer: []
    responses:
      200:
        description: login history
    """
    user_id = get_jwt()['id']

    try:
        history = []
        limit = settings.ROUTE_LOGIN_HISTORY_LIMIT_ROWS
        login_history = UserLoginRecord.query\
            .filter_by(user_id=user_id)\
            .order_by(desc(UserLoginRecord.login_at))\
            .limit(limit)
        for record in login_history:
            history.append({'date': record.login_at, 'user-agent': record.user_agent})

        return success('User login history', history)
    except Exception as e:
        return failed(str(e))
