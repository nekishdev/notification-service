import typing as t

from helpers.kafka import kafka_producer

from services.event_bus import EventBus


class KafkaEventBus(EventBus):
    def send(self, topic: str, msg_value: str, key: t.Optional[str] = None) -> None:
        _key = key.encode("utf-8") if key else None
        _value = msg_value.encode("utf-8")
        kafka_producer.send(topic=topic,
                            msg_value=_value,
                            key=_key)
