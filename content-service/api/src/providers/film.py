from functools import lru_cache

from fastapi import Depends

from db.elastic import get_elastic
from providers.cache import get_cache_repository
from repositories.cache import CacheRepository
from repositories.elastic_film import ElasticFilmRepository
from repositories.film import FilmRepository
from services.film import FilmService


async def get_film_repository() -> FilmRepository:
    return ElasticFilmRepository(await get_elastic(), 'movies')


@lru_cache()
def get_film_service(
    cache: CacheRepository = Depends(get_cache_repository),
    film_repository: FilmRepository = Depends(get_film_repository),
) -> FilmService:
    return FilmService(cache, film_repository)
