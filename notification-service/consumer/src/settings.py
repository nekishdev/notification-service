from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    EMAIL_SERVER: str
    EMAIL_PORT: int
    email_user: str
    email_password: str

    RABBITMQ_HOST: str
    RABBITMQ_QUEUE_NAME: str
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str

    class Config:
        env_file = "consumer/.env"
        env_file_encoding = "utf-8"


class PostgresSettings(BaseSettings):
    dbname: str = (Field(..., env="POSTGRES_DB"),)
    user: str = (Field(..., env="POSTGRES_USER"),)
    password: str = (Field(..., env="POSTGRES_PASSWORD"),)
    host: str = (Field(..., env="POSTGRES_HOST"),)
    port: int = Field(..., env="POSTGRES_CONTAINER_PORT")

    class Config:
        env_file = "consumer/.env"
        env_file_encoding = "utf-8"


settings = Settings()
pg_settings = PostgresSettings()
dsl = {
    "dbname": pg_settings.dbname,
    "user": pg_settings.user,
    "password": pg_settings.password,
    "host": pg_settings.host,
    "port": pg_settings.port,
}
