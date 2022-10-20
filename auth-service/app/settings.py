from datetime import timedelta

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(default='Auth service')
    APP_SECRET: str = Field()
    APP_DEBUG: bool = Field(default=False)

    APP_HOST: str = Field()
    APP_PORT: int = Field()

    REDIS_HOST: str = Field(default='127.0.0.1')
    REDIS_PORT: int = Field(default=6379)

    JAEGER_HOST: str = Field(default='localhost')
    JAEGER_PORT: int = Field(default=6831)
    JAEGER_ENABLE_TRACER: bool = Field(default=False)

    PG_DSN: str = Field()

    ACCESS_EXPIRES: timedelta = timedelta(minutes=15)
    REFRESH_EXPIRES: timedelta = timedelta(days=15)

    VK_OAUTH_URL: str
    VK_AUTH_CLIENT_ID: str
    VK_AUTH_CLIENT_SECRET: str
    VK_CALLBACK_URL: str

    YANDEX_OAUTH_URL: str
    YANDEX_AUTH_CLIENT_ID: str
    YANDEX_AUTH_CLIENT_SECRET: str
    YANDEX_CALLBACK_URL: str

    ROUTE_LOGIN_HISTORY_LIMIT_ROWS: str = Field(default=15)


settings = Settings()
