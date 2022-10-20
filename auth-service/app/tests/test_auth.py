import uuid
from datetime import datetime

from app import app


def is_uuid(val: str, version: int = 4) -> bool:
    try:
        uuid.UUID(val, version=version)
        return True
    except ValueError:
        return False


def create_user() -> dict:
    ts = str(datetime.now().timestamp())
    return {
        'login': f'test_user_{ts}',
        'password': f'test_pass_{ts}'
    }


def _test_register(user: dict) -> None:
    response = app.test_client().post('/api/v1/user/register', json=user)

    assert response.status_code == 200


def _test_login(user: dict) -> None:
    response = app.test_client().post('/api/v1/user/login', json=user)

    assert response.status_code == 200
    assert response.json.get('data').get('access_token') is not None


def _test_login_wrong_password(user: dict) -> None:
    response = app.test_client().post('/api/v1/user/login', json={
        'login': user['login'],
        'password': 'wrong-password'
    })

    assert response.status_code == 401
    assert response.json.get('success') is False
    assert response.json.get('message') == 'Wrong password'


def test_all():
    user = create_user()

    _test_register(user)

    _test_login(user)
    _test_login_wrong_password(user)
