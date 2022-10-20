from functools import lru_cache

from fastapi import Depends

from db.elastic import get_elastic
from providers.cache import get_cache_repository
from repositories.cache import CacheRepository
from repositories.elastic_person import ElasticPersonRepository
from repositories.person import PersonRepository
from services.person import PersonService


async def get_person_repository() -> PersonRepository:
    return ElasticPersonRepository(await get_elastic(), 'persons')


@lru_cache()
def get_person_service(
    cache: CacheRepository = Depends(get_cache_repository),
    person_repository: PersonRepository = Depends(get_person_repository),
) -> PersonService:
    return PersonService(cache, person_repository)
