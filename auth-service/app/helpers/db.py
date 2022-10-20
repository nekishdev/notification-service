from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

migrate = Migrate()


def db_init_app(app):
    db.init_app(app)
    migrate.init_app(app, db)
