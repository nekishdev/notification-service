import pytest

import orjson

from elasticsearch import AsyncElasticsearch

from core.config import settings

from http import HTTPStatus

SERVICE_URL = f'http://fastapi:{settings.FASTAPI_PORT}'


@pytest.mark.asyncio
async def test_validation_genre(genres_data, make_get_request, redis_client):
    """
    Тестирование /genres/search на правильность сортировки и количеству найденных по запросу жанров
    """

    # очистка кеша
    redis = await redis_client

    # 1. проверка поиска по количеству добавленных и найденных записей
    await redis.flushall()
    search_phrase = 'genre for test 4'
    response = await make_get_request(
        '/genres/search', {'query': search_phrase, 'page_size': 100}
    )

    assert response.status == HTTPStatus.OK
    assert (len(response.body) == 26) and (
        response.body[0]['name'] == search_phrase
    ), 'Количество найденных данных отличается от ожидаемого'

    # 2. проверка сортировки
    await redis.flushall()
    response = await make_get_request(
        '/genres/search', {'query': 'genre for test ', 'page_size': 100, 'sort': '-name'}
    )

    assert response.status == HTTPStatus.OK
    assert response.body[-1]['id'] == genres_data[3]['id'], 'Тест на сортировку не пройден'


@pytest.mark.asyncio
async def test_search_genre(genres_data, make_get_request, redis_client):
    """
    Тест на поиск конкретного жанра по id
    """

    # очистка кеша
    redis = await redis_client
    await redis.flushall()

    expected = genres_data[11]

    # Выполнение запроса через апи
    response = await make_get_request('/genres/' + expected['id'])

    # Проверка результата
    assert response.status == HTTPStatus.OK
    assert (
        response.body['id'] == expected['id'] and response.body['name'] == expected['name']
    ), 'Найденные данные отличаются от ожидаемых'


@pytest.mark.asyncio
async def test_count_and_print_genres(
    es_client: AsyncElasticsearch, make_get_request, redis_client
):
    """
    Тест на вывод всех жанров
    """

    # очистка кеша
    redis = await redis_client
    await redis.flushall()

    genres_count = await es_client.count(body=None, index='genres')

    page_size = 10
    page_number = 1
    data_exists = True
    count_items = 0
    while data_exists:
        response = await make_get_request(
            '/genres/search',
            {'page_size': page_size, 'page_number': page_number, 'sort': 'name'},
        )
        count_items += len(response.body)
        data_exists = (response.status == HTTPStatus.OK) and (len(response.body) >= page_size)

        assert response.status == HTTPStatus.OK

        if data_exists:
            page_number += 1
    assert count_items == genres_count['count'], 'Найдены не все данные о жанрах'


@pytest.mark.asyncio
async def test_search_genre_check_redis(
    genres_data, make_get_request, redis_client, make_redis_request
):
    """
    Тест на поиск конкретного жанра в кеше Redis
    """

    # очистка кеша
    redis = await redis_client
    await redis.flushall()

    expected = genres_data[1]

    # Выполнение запроса через апи
    response = await make_get_request('/genres/' + expected['id'])

    # Проверка результата
    assert response.status == HTTPStatus.OK

    # запрос данных в кеше
    redis_data = await make_redis_request('genres_detail_genre_id_' + expected['id'])
    item_from_redis = orjson.loads(redis_data)

    assert item_from_redis == [expected], 'Найденные в кеше данные отличаются от ожидаемых'
