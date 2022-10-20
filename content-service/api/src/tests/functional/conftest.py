import aiohttp
import pytest
import aioredis
import asyncio

from typing import Optional
from dataclasses import dataclass
from multidict import CIMultiDictProxy
from elasticsearch import AsyncElasticsearch, ElasticsearchException

import backoff

# import redis

from uuid import uuid4


from core.config import settings

SERVICE_URL = f'http://fastapi:{settings.FASTAPI_PORT}'


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture
def event_loop():
    yield asyncio.get_event_loop()


@backoff.on_exception(backoff.expo, ElasticsearchException, max_time=60)
async def check_elasticsearch_is_ready(es_client):
    res = await es_client.ping()
    if res is False:
        raise ElasticsearchException
    return res


@pytest.fixture(scope='session')
async def es_client():
    host = f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}'
    client = AsyncElasticsearch(hosts=host)
    await check_elasticsearch_is_ready(client)
    yield client
    await client.close()


@backoff.on_exception(backoff.expo, BaseException, max_time=60)
async def redis_is_ready():
    r = await aioredis.create_redis((settings.REDIS_HOST, settings.REDIS_PORT))
    await r.ping()
    r.quit()


@pytest.fixture(scope='session')
async def redis_client():
    await redis_is_ready()
    redis = await aioredis.create_redis_pool(
        (settings.REDIS_HOST, settings.REDIS_PORT), minsize=10, maxsize=20
    )
    yield redis
    redis.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        url = SERVICE_URL + '/api/v1' + method  # в боевых системах старайтесь так не делать!
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(), headers=response.headers, status=response.status,
            )

    return inner


@pytest.fixture
def make_redis_request(redis_client):
    async def inner(key: str):
        with await redis_client as redis:
            return await redis.get(key)

    return inner


@pytest.fixture(scope='session')
async def persons_data(es_client):
    index_name = 'persons'

    test_person = {'id': str(uuid4()), 'full_name': 'Константин Хабенский'}
    es_data = [{'index': {'_index': index_name, '_id': test_person['id']}}, test_person]
    del_data = [{'delete': {'_index': index_name, '_id': test_person['id']}}]

    items_count = 117
    for i in range(items_count):
        expected = {'id': str(uuid4()), 'full_name': 'Person for test ' + str(i)}
        es_data += [{'index': {'_index': index_name, '_id': expected['id']}}, expected]
        del_data += [{'delete': {'_index': index_name, '_id': expected['id']}}]

    try:
        # добавление данных в elasticsearch для дальнейшего поиска через апи
        await es_client.bulk(es_data, refresh=True)
        yield es_data
    finally:
        await es_client.bulk(del_data, refresh=True)


@pytest.fixture(scope='session')
async def genres_data(es_client):
    index_name = 'genres'
    items_count = 26

    expected = {'id': str(uuid4()), 'name': 'Трагикомедия', 'description': 'test'}
    es_data = [{'index': {'_index': index_name, '_id': expected['id']}}, expected]
    del_data = [{'delete': {'_index': index_name, '_id': expected['id']}}]

    for i in range(items_count):
        expected = {
            'id': str(uuid4()),
            'name': 'genre for test ' + str(i),
            'description': 'Description' + str(i),
        }
        es_data += [{'index': {'_index': index_name, '_id': expected['id']}}, expected]
        del_data += [{'delete': {'_index': index_name, '_id': expected['id']}}]

    try:
        # добавление данных в elasticsearch для дальнейшего поиска через апи
        await es_client.bulk(es_data, refresh=True)
        yield es_data
    finally:
        await es_client.bulk(del_data, refresh=True)


@pytest.fixture(scope='session')
async def movies_data(es_client, persons_data):
    index_name = 'movies'

    test_person = persons_data[1]

    expected1 = {
        'id': str(uuid4()),
        'imdb_rating': 3.0,
        'genre_names': ['Комедия'],
        'genres': [{'id': 'a2cdde28-76e8-4ead-ac81-ac5cc698c759', 'name': 'Комедия'}],
        'title': 'Star wars with Habenskiy',
        'description': 'Very test film about great work of actor in comedy films',
        'director_names': [],
        'actors_names': ['Константин Хабенский'],
        'writers_names': [],
        'directors': [],
        'actors': [test_person],
        'writers': [],
    }

    expected2 = {
        'id': str(uuid4()),
        'imdb_rating': 8.0,
        'genre_names': ['Трагикомедия'],
        'genres': [{'id': 'a2cdde28-76e8-4ead-ac81-ac5cc698c759', 'name': 'Трагикомедия'}],
        'title': 'Star wars with Habenskiy',
        'description': 'Very test film about great work of actor in comedy films',
        'director_names': [],
        'actors_names': ['Константин Хабенский'],
        'writers_names': [],
        'directors': [],
        'actors': [test_person],
        'writers': [],
    }

    expected3 = {
        'id': str(uuid4()),
        'imdb_rating': 4.0,
        'genre_names': ['Комедия'],
        'genres': [{'id': 'a2cdde28-76e8-4ead-ac81-ac5cc698c759', 'name': 'Комедия'}],
        'title': 'Star wars evolution',
        'description': 'Very test film',
        'director_names': [],
        'actors_names': ['Константин Хабенский'],
        'writers_names': [],
        'directors': [],
        'actors': [test_person],
        'writers': [],
    }

    expected4 = {
        'id': str(uuid4()),
        'imdb_rating': 8.0,
        'genre_names': ['Комедия'],
        'genres': [{'id': 'a2cdde28-76e8-4ead-ac81-ac5cc698c759', 'name': 'Комедия'}],
        'title': 'Star wars evolution 2',
        'description': 'Very test film',
        'director_names': [],
        'actors_names': ['Константин Хабенский'],
        'writers_names': [],
        'directors': [],
        'actors': [test_person],
        'writers': [],
    }

    es_data = [
        {'index': {'_index': index_name, '_id': expected1['id']}},
        expected1,
        {'index': {'_index': index_name, '_id': expected2['id']}},
        expected2,
        {'index': {'_index': index_name, '_id': expected3['id']}},
        expected3,
        {'index': {'_index': index_name, '_id': expected4['id']}},
        expected4,
    ]

    del_data = []
    for item in es_data:
        if 'index' in item:
            del_data += [{'delete': {'_index': index_name, '_id': item['index']['_id']}}]

    try:
        # добавление данных в elasticsearch для дальнейшего поиска через апи
        await es_client.bulk(es_data, refresh=True)
        yield es_data
    finally:
        await es_client.bulk(del_data, refresh=True)
