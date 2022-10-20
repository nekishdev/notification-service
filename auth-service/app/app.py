from flasgger import Swagger
from flask import Flask

from blueprints.v1.router import v1_router
from commands import setup_cli_commands
from helpers.db import db_init_app
from helpers.jaeger import configure_jaeger
from helpers.jwt import jwt_init_app
from settings import settings
from swagger import swagger_spec

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{settings.PG_DSN}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = settings.APP_SECRET
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = settings.ACCESS_EXPIRES
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = settings.REFRESH_EXPIRES

db_init_app(app)
jwt_init_app(app)
setup_cli_commands(app)
configure_jaeger(app)
swagger = Swagger(app, template=swagger_spec)

app.register_blueprint(v1_router, url_prefix='/api/v1')


if __name__ == '__main__':
    app.run(
        load_dotenv=False,
        debug=settings.APP_DEBUG,
        host=settings.APP_HOST,
        port=settings.APP_PORT
    )
