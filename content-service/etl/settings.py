from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    PG_DSN: PostgresDsn

    ELASTIC_HOST: str = '127.0.0.1'
    ELASTIC_PORT: int = 9200
    ELASTIC_MOVIES_INDEX_NAME: str = 'movies'
    ELASTIC_GENRES_INDEX_NAME: str = 'genres'
    ELASTIC_PERSONS_INDEX_NAME: str = 'persons'

    class Config:
        case_sensitive = True
        env_file = 'etl/.env'
        env_file_encoding = 'utf-8'



settings = Settings()
