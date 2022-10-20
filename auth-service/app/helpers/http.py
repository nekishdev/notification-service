import datetime
from functools import wraps
from http import HTTPStatus

from flask import jsonify, request
from flask_jwt_extended import get_jwt

from helpers.redis import redis_conn


def abort(status: int, message: str):
    return jsonify({
        'success': False,
        'message': message
    }), status


def success(message: str, data=None):
    if data is not None:
        return jsonify(
            success=True, 
            message=message,
            data=data
        )
    else:
        return jsonify(
            success=True, 
            message=message,
        )


def failed(message: str, status: int = 400):
    return jsonify({
        'success': False,
        'message': message
    }), status


def admin_required():
    def wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            roles = get_jwt().get('roles') or []
            if 'Admin' not in roles:
                return abort(403, 'Operation is not permitted')
            result = f(*args, **kwargs)
            return result
        return inner
    return wrapper


def rate_limit(limit=1000, interval=60):
    """Rate limiter."""

    def rate_limit_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key: str = f"Limit::{request.remote_addr}:{datetime.datetime.now().minute}"
            current_request_count = redis_conn.get(key=key)

            if current_request_count and int(current_request_count) >= limit:
                return {
                           "message": f"Too many requests. Limit {limit} in {interval} seconds",
                       }, HTTPStatus.TOO_MANY_REQUESTS

            else:
                pipe = redis_conn.pipeline()
                pipe.incr(key, 1)
                pipe.expire(key, interval + 1)
                pipe.execute()

                return func(*args, **kwargs)

        return wrapper

    return rate_limit_decorator
