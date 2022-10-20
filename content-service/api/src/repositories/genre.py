import uuid
from abc import ABC, abstractmethod
from typing import List, Optional

from models.genre import Genre


class GenreRepository(ABC):
    """
    Интерфейс хранилища жанров.
    """

    @abstractmethod
    def get_by_id(self, doc_id: uuid.UUID):
        pass

    @abstractmethod
    async def all(self) -> List[Genre]:
        pass

    @abstractmethod
    async def filter(
        self,
        *,
        sort: Optional[str] = None,
        page_size: Optional[int] = None,
        page_number: Optional[int] = None,
        search_phrase: Optional[str] = None
    ) -> List[Genre]:
        pass
