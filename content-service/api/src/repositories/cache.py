from abc import ABC, abstractmethod
from typing import Any


class CacheRepository(ABC):
    """
    Интерфейс для кеша.
    """

    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, key: str, value: Any, expire: int = 0):
        pass
