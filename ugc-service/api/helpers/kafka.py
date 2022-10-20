from kafka import KafkaProducer
from settings import settings

config = {
    "bootstrap_servers": [settings.KAFKA_BROKER_URL]
}
if settings.KAFKA_API_VERSION:
    config["api_version"] = settings.API_VERSION

kafka_producer = KafkaProducer(**config)
