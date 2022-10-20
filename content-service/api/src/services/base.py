from typing import List, Union

from pydantic import BaseModel

import orjson

from repositories.cache import CacheRepository
from helpers.orjson import dumps_model_list


class BaseService:
    def __init__(self, cache: CacheRepository, model: BaseModel):
        self.model = model
        self.cache_index: str = ''
        self.CACHE_EXPIRED: int = 5 * 60
        self.cache: CacheRepository = cache

    async def _get_list_from_cache(self, key: str) -> List[BaseModel]:
        data = await self.cache.get(key)
        if not data:
            return []

        items = orjson.loads(data)

        list_items = [self.model(**i) for i in items]
        return list_items

    async def _get_one_from_cache(self, key: str) -> Union[BaseModel, None]:
        items = await self._get_list_from_cache(key)
        for i in items:
            return i
        return None

    async def _put_list_to_cache(self, key: str, list_items: List[BaseModel]):
        value = dumps_model_list(list_items)
        await self.cache.set(key, value, expire=self.CACHE_EXPIRED)

    def _prepare_cache_key(self, key: str) -> str:
        return f'{self.cache_index}_{key}'
