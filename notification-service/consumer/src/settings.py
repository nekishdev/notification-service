from pydantic import BaseSettings, Field


class CommonSettings(BaseSettings):
    TESTING: bool


class Settings(CommonSettings):
    EMAIL_SERVER: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str

    RABBITMQ_HOST: str
    RABBITMQ_QUEUE_NAME: str
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str

    MAILHOG_HOST: str
    MAILHOG_PORT: int

    class Config:
        env_file = "consumer/.env"
        env_file_encoding = "utf-8"


class PostgresSettings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_CONTAINER_PORT: int

    class Config:
        env_file = "consumer/.env"
        env_file_encoding = "utf-8"


settings = Settings()
pg_settings = PostgresSettings()
dsl = {
    "dbname": pg_settings.POSTGRES_DB,
    "user": pg_settings.POSTGRES_USER,
    "password": pg_settings.POSTGRES_PASSWORD,
    "host": pg_settings.POSTGRES_HOST,
    "port": pg_settings.POSTGRES_CONTAINER_PORT
}
