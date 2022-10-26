import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(default="API сервиса нотификации")

    DEBUG: bool = Field(default=False)

    FASTAPI_HOST: str = Field(default="127.0.0.1")
    FASTAPI_PORT: int = Field(default=8000)

    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_QUEUE_NAME: str

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class JwtSettings(BaseSettings):
    AUTHJWT_SECRET_KEY: str = "secret-1qaz!QAZ"


settings = Settings()
