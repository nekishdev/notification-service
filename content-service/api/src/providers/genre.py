from functools import lru_cache

from fastapi import Depends

from db.elastic import get_elastic
from providers.cache import get_cache_repository
from repositories.cache import CacheRepository
from repositories.elastic_genre import ElasticGenreRepository
from repositories.genre import GenreRepository
from services.genre import GenreService


async def get_genre_repository() -> GenreRepository:
    return ElasticGenreRepository(await get_elastic(), 'genres')


@lru_cache()
def get_genre_service(
    cache: CacheRepository = Depends(get_cache_repository),
    genre_repository: GenreRepository = Depends(get_genre_repository),
) -> GenreService:
    return GenreService(cache, genre_repository)
