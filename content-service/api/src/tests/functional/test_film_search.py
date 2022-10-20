import pytest

from dataclasses import dataclass
from multidict import CIMultiDictProxy
from elasticsearch import AsyncElasticsearch

from orjson import loads as json_load

from core.config import settings

from http import HTTPStatus

SERVICE_URL = f'http://fastapi:{settings.FASTAPI_PORT}'


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.mark.asyncio
@pytest.mark.test_backof
async def test_search_detailed(movies_data, make_get_request, redis_client):
    """
    Тест поиска фильма по названию, описанию, участнику
    """

    # очистка кеша
    redis = await redis_client
    await redis.flushall()

    expected = movies_data[1]

    # Поиск по названию
    response = await make_get_request('/films/search', {'query': 'with Habenskiy'})

    assert response.status == HTTPStatus.OK
    assert len(response.body) == 2
    assert response.body[0] == expected

    # Поиск по описанию
    response = await make_get_request(
        '/films/search', {'query': 'great work', 'page_size': 100}
    )

    assert response.status == HTTPStatus.OK
    assert len(response.body) == 59
    assert response.body[0] == expected

    # Поиск по участнику
    response = await make_get_request('/films/search', {'query': 'Константин'})

    assert response.status == HTTPStatus.OK
    assert len(response.body) == 1
    assert response.body[0] == expected


@pytest.mark.asyncio
async def test_get_all_films(es_client: AsyncElasticsearch, make_get_request, redis_client):
    """
    Тест вывода всех кинопроизведений
    """

    # очистка кеша
    redis = await redis_client
    await redis.flushall()

    films_count = await es_client.count(body=None, index='movies')

    page_size = 100
    page_number = 1
    data_exists = True
    count_items = 0
    while data_exists:
        response = await make_get_request(
            '/films/',
            {'page_size': page_size, 'page_number': page_number, 'sort': 'title.raw'},
        )
        count_items += len(response.body)
        data_exists = (response.status == HTTPStatus.OK) and (len(response.body) >= page_size)

        assert response.status == HTTPStatus.OK

        if data_exists:
            page_number += 1

    assert count_items == films_count['count'], 'Найдены не все данные о кинопроизведениях'


@pytest.mark.asyncio
async def test_get_film_by_id(make_get_request, redis_client):
    """
    Тест поиска кинопроизведения по идентификатору
    """

    # очистка кеша
    redis = await redis_client
    await redis.flushall()

    # поиск
    expected_data = {
        'id': '86607a8f-bc90-47fa-8261-15647186cbf5',
        'title': '50 Years of Star Trek',
        'description': 'The cast , crew , creators & critics discuss the impact of Star Trek from its creation by Gene Roddenberry to the present into today and the future. Showing clips from the original unaired pilot featuring Jeffery Hunter from 1965 to 9/8/1966 the 1st show aired. 50 years of dialog, the movies and what we can expect next.',
        'imdb_rating': 7,
        'genres': [
            {'id': '6c162475-c7ed-4461-9184-001ef3d9f26e', 'name': 'Sci-Fi'},
            {'id': '6d141ad2-d407-4252-bda4-95590aaf062a', 'name': 'Documentary'},
        ],
        'genre_names': ['Sci-Fi', 'Documentary'],
        'directors': [
            {'id': 'a68120b5-8e04-4020-ab55-3cff9d1403b8', 'full_name': 'Ian Roumain'}
        ],
        'actors': [
            {'id': '65e38201-f416-4176-b24e-ed0c89e1f2b5', 'full_name': 'Mark A. Altman'},
            {'id': '83e09e52-4a63-49f9-8c34-3d09774f7509', 'full_name': 'Robert Beltran'},
            {'id': 'a1758395-9578-41af-88b8-3f9456e6d938', 'full_name': 'J.J. Abrams'},
            {'id': 'dcd7a871-efc0-4ddb-a073-6fa8932b24f4', 'full_name': 'John Barrowman'},
        ],
        'writers': [
            {'id': '5716d5e5-2c4f-46b0-b6e5-a006f049bdcb', 'full_name': 'Joe Braswell'}
        ],
        'director_names': ['Ian Roumain'],
        'actors_names': ['Mark A. Altman', 'Robert Beltran', 'J.J. Abrams', 'John Barrowman'],
        'writers_names': ['Joe Braswell'],
    }

    response = await make_get_request('/films/' + expected_data['id'])

    assert response.status == HTTPStatus.OK

    assert response.body == expected_data, 'Найденные данные отличаются от ожидаемых'


@pytest.mark.asyncio
async def test_search_film_in_cache(
    movies_data, make_get_request, redis_client, make_redis_request
):
    """
    Тест поиска кинопроизведения в кеше
    """

    # очистка кеша
    redis = await redis_client
    await redis.flushall()

    expected = movies_data[3]

    response = await make_get_request('/films/' + expected['id'])

    assert response.status == HTTPStatus.OK

    # запрос данных в кеше
    redis_data = await make_redis_request('movies_detail_film_id_' + expected['id'])
    item_from_redis = json_load(redis_data)

    assert (
        item_from_redis[0]['id'] == expected['id']
        and item_from_redis[0]['title'] == expected['title']
        and item_from_redis[0]['description'] == expected['description']
    ), 'Найденные в кеше данные отличаются от ожидаемых'
