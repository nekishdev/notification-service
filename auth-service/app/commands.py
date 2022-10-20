import click
from flask import Flask

from helpers.db import db
from models.models import Role, User


def setup_cli_commands(app: Flask) -> None:
    @app.cli.command("create-super-user")
    @click.argument("login")
    @click.argument("password")
    def create_user(login: str, password: str):
        admin_role = Role(name='Admin')
        user = User(login=login,
                    password=password,
                    roles=[admin_role])

        db.session.add(user)
        db.session.commit()
