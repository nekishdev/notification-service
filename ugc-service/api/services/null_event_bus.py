import typing as t

from services.event_bus import EventBus


class NullEventBus(EventBus):
    def send(self, topic: str, msg_value: str, key: t.Optional[str] = None) -> None:
        """This class method do nothing."""
