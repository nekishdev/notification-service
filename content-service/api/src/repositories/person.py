import uuid
from abc import ABC, abstractmethod
from typing import Optional, List

from models.person import Person


class PersonRepository(ABC):
    """
    Интерфейс хранилища персон.
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
        search_phrase: Optional[str] = None
    ) -> List[Person]:
        pass
