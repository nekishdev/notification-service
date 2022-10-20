import uuid
from abc import ABC, abstractmethod
from typing import Optional, List

from models.film import Film


class FilmRepository(ABC):
    """
    Интерфейс хранилища фильмов.
    """

    @abstractmethod
    def get_by_id(self, doc_id: uuid.UUID):
        pass

    @abstractmethod
    async def filter(
        self,
        *,
        sort: Optional[str] = None,
        page_size: Optional[int] = None,
        page_number: Optional[int] = None,
        search_phrase: Optional[str] = None,
        genre_id: Optional[uuid.UUID] = None,
        person_id: Optional[uuid.UUID] = None
    ) -> List[Film]:
        pass
