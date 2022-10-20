import helpers.mongo as mongo_helper
import sentry_sdk
from blueprints.v1.router import v1_router
from flasgger import Swagger
from flask import Flask
from helpers.jwt import jwt_init_app
from sentry_sdk.integrations.flask import FlaskIntegration
from settings import settings
from swagger import swagger_spec

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    integrations=[
        FlaskIntegration(),
    ],
    traces_sample_rate=1.0,
)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = settings.APP_SECRET

jwt_init_app(app)
mongo_helper.ensure_collections_exists()
swagger = Swagger(app, template=swagger_spec)

app.register_blueprint(v1_router, url_prefix="/api/v1")

if __name__ == "__main__":
    app.run(debug=settings.APP_DEBUG, host=settings.APP_HOST, port=settings.APP_PORT)
