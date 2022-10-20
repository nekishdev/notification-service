import typing as t

import abc


class EventBus(abc.ABC):
    @abc.abstractmethod
    def send(self,
             topic: str,
             msg_value: str,
             key: t.Optional[str] = None) -> None:
        """Just abstract method definition."""
