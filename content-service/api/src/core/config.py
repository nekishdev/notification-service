import os
from logging import config as logging_config

from core.logger import LOGGING

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(default='Read-only API для онлайн-кинотеатра')

    DEBUG: bool = Field(default=False)

    FASTAPI_HOST: str = Field(default='127.0.0.1')
    FASTAPI_PORT: int = Field(default=8000)

    REDIS_HOST: str = Field(default='127.0.0.1')
    REDIS_PORT: int = Field(default=6379)

    ELASTIC_HOST: str = Field(default='127.0.0.1')
    ELASTIC_PORT: int = Field(default=9200)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class JwtSettings(BaseSettings):
    AUTHJWT_SECRET_KEY: str = "secret"


logging_config.dictConfig(LOGGING)

settings = Settings()
