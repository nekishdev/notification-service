import logging
import sys

from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    batch_size: int = Field(1000)


class KafkaSettings(BaseSettings):
    uri: list[str] = Field(["localhost:29092"])
    topics: str = Field("views")
    group_id: str = Field("echo-messages-to-stdout")

    class Config:
        env_prefix = "kafka_"


class ClickHouseSettings(BaseSettings):
    host: str = Field("localhost")
    port: str = Field("9000")
    db: str = Field("content")
    tables: list[str] = Field(["views"])

    class Config:
        env_prefix = "ch_"


class Settings(BaseSettings):
    app = AppSettings()
    kafka = KafkaSettings()
    ch = ClickHouseSettings()


settings = Settings()

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
