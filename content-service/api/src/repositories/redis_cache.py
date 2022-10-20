from typing import Any

from aioredis import Redis

from repositories.cache import CacheRepository


class RedisCacheRepository(CacheRepository):
    """
    Класс для работы с кешем в Redis.
    """

    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str):
        return await self.redis.get(key)

    async def set(self, key: str, value: Any, *, expire: int = 0):
        await self.redis.set(key, value, expire=expire)
