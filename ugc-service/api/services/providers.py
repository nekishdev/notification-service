from settings import settings

from services.event_bus import EventBus


def get_event_bus() -> EventBus:
    _type: str = settings.EVENT_BUS_TYPE
    if _type == "kafka":
        from services.kafka_event_bus import KafkaEventBus
        return KafkaEventBus()
    elif _type == "null":
        from services.null_event_bus import NullEventBus
        return NullEventBus()
    else:
        raise NotImplementedError(f"Event bus with type [{_type}] is not implemented")
