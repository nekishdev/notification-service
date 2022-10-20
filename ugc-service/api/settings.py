from typing import Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(default='UGC API Service')

    SWAGGER_HOST: str

    APP_SECRET: str = Field(default='super-secret')
    APP_DEBUG: bool = Field(default=False)

    APP_HOST: str
    APP_PORT: int

    MONGO_DSN: str

    EVENT_BUS_TYPE: str = Field(default='kafka')
    KAFKA_BROKER_URL: str = Field(default='localhost:9092')
    KAFKA_API_VERSION: Optional[str]
    KAFKA_TOPIC_VIEWS: str = Field(default='views')

    SENTRY_DSN: str


settings = Settings()
