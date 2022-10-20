import uuid
from typing import Optional, List

from models.genre import Genre
from repositories.cache import CacheRepository
from repositories.genre import GenreRepository
from services.base import BaseService

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class GenreService(BaseService):
    def __init__(self, cache: CacheRepository, genre_repository: GenreRepository):
        super().__init__(cache, Genre)
        self.cache_index: str = 'genres'
        self._repository = genre_repository

    async def get_all(self) -> List[Genre]:
        cache_key = self._prepare_cache_key('all')

        docs = await self._get_list_from_cache(cache_key)
        if not docs:
            docs = await self._repository.all()
            if not docs:
                return []

            await self._put_list_to_cache(cache_key, docs)

        return docs

    async def search(
        self,
        query: Optional[str],
        sort: Optional[str],
        page_size: int = 20,
        page_number: int = 1,
    ) -> List[Genre]:
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

    async def detail(self, genre_id: uuid.UUID) -> Optional[Genre]:
        cache_key_list = ['detail', 'genre_id', str(genre_id)]
        cache_key = self._prepare_cache_key('_'.join(cache_key_list))

        doc = await self._get_one_from_cache(cache_key)
        if not doc:
            doc = await self._repository.get_by_id(genre_id)
            if not doc:
                return None

            await self._put_list_to_cache(cache_key, [doc])

        return doc
