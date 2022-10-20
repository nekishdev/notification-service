import uuid
from typing import Optional, List

from models.film import Film
from repositories.cache import CacheRepository
from repositories.film import FilmRepository
from services.base import BaseService


class FilmService(BaseService):
    def __init__(self, cache: CacheRepository, film_repository: FilmRepository):
        super().__init__(cache, Film)
        self.cache_index: str = 'movies'
        self._repository: FilmRepository = film_repository

    async def get_by_id(self, film_id: uuid.UUID) -> Optional[Film]:
        cache_key_list = ['detail', 'film_id', str(film_id)]
        cache_key = self._prepare_cache_key('_'.join(cache_key_list))

        film = await self._get_one_from_cache(cache_key)
        if not film:
            film = await self._repository.get_by_id(film_id)
            if not film:
                return None

            await self._put_list_to_cache(cache_key, [film])

        return film

    async def get_list(
        self,
        sort: Optional[str],
        page_size: int = 20,
        page_number: int = 1,
        genre_id: Optional[uuid.UUID] = None,
        person_id: Optional[uuid.UUID] = None,
    ) -> List[Film]:
        cache_key_list = [
            'list',
            'sort',
            str(sort),
            'page_size',
            str(page_size),
            'page_number',
            str(page_number),
            'genre_id',
            str(genre_id),
            'person_id',
            str(person_id),
        ]
        cache_key = self._prepare_cache_key('_'.join(cache_key_list))

        films = await self._get_list_from_cache(cache_key)

        if not films:
            films = await self._repository.filter(
                sort=sort,
                page_size=page_size,
                page_number=page_number,
                genre_id=genre_id,
                person_id=person_id,
            )

            if not films:
                return []

            await self._put_list_to_cache(cache_key, films)

        return films

    async def search(
        self, query: str, sort: Optional[str], page_size: int = 20, page_number: int = 1
    ):
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

        films = await self._get_list_from_cache(cache_key)
        if not films:
            films = await self._repository.filter(
                sort=sort, page_size=page_size, page_number=page_number, search_phrase=query
            )
            if not films:
                return []

            await self._put_list_to_cache(cache_key, films)

        return films
