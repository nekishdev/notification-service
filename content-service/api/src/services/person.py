import uuid
from typing import Optional, List

from models.person import Person
from repositories.cache import CacheRepository
from repositories.person import PersonRepository
from services.base import BaseService


class PersonService(BaseService):
    def __init__(self, cache: CacheRepository, person_repository: PersonRepository):
        super().__init__(cache, Person)
        self.cache_index: str = 'persons'
        self._repository = person_repository

    async def search(
        self,
        query: Optional[str],
        sort: Optional[str],
        page_size: int = 20,
        page_number: int = 1,
    ) -> List[Person]:
        error = None
        cache_key_list = [
            'search',
            'query',
            str(query),
            'sort',
            str(sort),
            'page_size',
            str(page_size),
            'page_number',
            str(page_number),
        ]
        cache_key = self._prepare_cache_key('_'.join(cache_key_list))

        docs = await self._get_list_from_cache(cache_key)
        if not docs:
            docs, error = await self._repository.filter(
                sort=sort, page_size=page_size, page_number=page_number, search_phrase=query
            )
            if not docs:
                return [], error

            await self._put_list_to_cache(cache_key, docs)

        return docs, error

    async def detail(self, person_id: uuid.UUID) -> Optional[Person]:
        cache_key_list = ['detail', 'person_id', str(person_id)]
        cache_key = self._prepare_cache_key('_'.join(cache_key_list))

        doc = await self._get_one_from_cache(cache_key)
        if not doc:
            doc = await self._repository.get_by_id(person_id)
            if not doc:
                return None

            await self._put_list_to_cache(cache_key, [doc])

        return doc
