from flask_jwt_extended import JWTManager

jwt = JWTManager()


def jwt_init_app(app):
    jwt.init_app(app)
