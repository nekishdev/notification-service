from flask import Blueprint

from blueprints.v1.role import role_router
from blueprints.v1.social_auth import auth_router
from blueprints.v1.user import user_router
from helpers.http import rate_limit

v1_router = Blueprint('v1', __name__)
v1_router.register_blueprint(user_router, url_prefix='/user')
v1_router.register_blueprint(role_router, url_prefix='/role')
v1_router.register_blueprint(auth_router, url_prefix='/auth')


@v1_router.before_request
# @rate_limit
def before_request():
    pass
