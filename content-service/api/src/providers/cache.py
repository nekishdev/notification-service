from db.redis import get_redis
from repositories.cache import CacheRepository
from repositories.redis_cache import RedisCacheRepository


async def get_cache_repository() -> CacheRepository:
    return RedisCacheRepository(await get_redis())
