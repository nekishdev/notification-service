import pytest

import orjson

from elasticsearch import AsyncElasticsearch

from core.config import settings

from http import HTTPStatus

SERVICE_URL = f'http://fastapi:{settings.FASTAPI_PORT}'


@pytest.mark.asyncio
@pytest.mark.pv
async def test_validation_search_person(persons_data, make_get_request, redis_client):
    """
    Тестирование правильности сортировки, сортировки по неразрешенному полю, по количеству найденных по запросу людей
    """

    # очистка кеша
    redis = await redis_client

    persons_count_expected = len(persons_data) // 2 - 1

    # 1. проверка поиска по количеству добавленых и найденных записей
    await redis.flushall()
    page_size = 100
    page_number = 1

    data_exists = True
    count_items = 0
    while data_exists:
        response = await make_get_request(
            '/persons/search',
            {
                'query': 'test',
                'page_size': page_size,
                'page_number': page_number,
                'sort': '-full_name.raw',
            },
        )
        count_items += len(response.body)
        data_exists = (response.status == HTTPStatus.OK) and (len(response.body) >= page_size)

        assert response.status == HTTPStatus.OK

        if data_exists:
            page_number += 1
    assert (
        count_items == persons_count_expected
    ), 'Количество найденных данных отличается от ожидаемого'

    # 2. проверка сортировки
    assert response.body[-1]['id'] == persons_data[3]['id'], 'Тест на сортировку не пройден'

    # 3. проверка сортировки по 'неразрешенному' полю
    await redis.flushall()
    response = await make_get_request(
        '/persons/search', {'query': 'test', 'size': 250, 'sort': 'created_at'}
    )
    assert response.status == HTTPStatus.BAD_REQUEST


# @pytest.mark.asyncio
# async def test_validation_search_person(es_client: AsyncElasticsearch, make_get_request, redis_client):
#     """
#     Тестирование правильности сортировки, сортировки по неразрешенному полю, по количеству найденных по запросу людей
#     """

#     # очистка кеша
#     redis = await redis_client

#     persons_count_expected = 5
#     es_data = []
#     for i in range(persons_count_expected):
#         expected = {'id': str(uuid4()), 'full_name': 'Person for test ' + str(i)}
#         es_data += [{'index': {'_index': 'persons', '_id': expected['id']}}, expected]

#     try:
#         # добавление данных в elasticsearch для дальнейшего поиска через апи
#         await es_client.bulk(es_data, refresh=True)

#         # 1. проверка поиска по количеству добавленых и найденных записей
#         await redis.flushall()
#         response = await make_get_request('/persons/search', {'query': 'test', 'size': 250})

#         assert response.status == HTTPStatus.OK
#         assert (
#             len(response.body) == persons_count_expected
#         ), 'Количество найденных данных отличается от ожидаемого'

#         # 2. проверка сортировки
#         await redis.flushall()
#         response = await make_get_request(
#             '/persons/search', {'query': 'test', 'size': 250, 'sort': '-full_name.raw'}
#         )

#         assert response.status == HTTPStatus.OK
#         assert (
#             response.body[0]['id'] == es_data[persons_count_expected * 2 - 1]['id']
#         ), 'Тест на сортировку не пройден'

#         # 3. проверка сортировки по 'неразрешенному' полю
#         await redis.flushall()
#         response = await make_get_request(
#             '/persons/search', {'query': 'test', 'size': 250, 'sort': 'created_at'}
#         )
#         assert response.status == HTTPStatus.BAD_REQUEST
#     finally:
#         for item in es_data:
#             if 'id' in item:
#                 await es_client.delete(index='persons', id=item['id'], refresh=True)


@pytest.mark.asyncio
async def test_search_person(persons_data, make_get_request, redis_client):
    """
    Тест на поиск конкретного человека по id
    """

    redis = await redis_client

    expected = persons_data[3]

    await redis.flushall()
    # 1. проверка поиска по количеству добавленых и найденных записей
    response = await make_get_request('/persons/' + expected['id'])

    assert response.status == HTTPStatus.OK
    assert response.body == expected, 'Результат поиска отличается от ожидаемого'


@pytest.mark.asyncio
async def test_search_film_person(
    persons_data, es_client: AsyncElasticsearch, make_get_request, redis_client
):
    """
    Тест на поиск фильмов с участием конкретного человека
    """

    redis = await redis_client
    await redis.flushall()

    # подготовка тестовых данных
    test_person = persons_data[1]

    # 1. проверка поиска по количеству добавленых и найденных записей
    # Выполнение запроса через апи
    response = await make_get_request('/persons/' + test_person['id'] + '/film')

    # Проверка результата
    assert response.status == HTTPStatus.OK
    assert len(response.body) == 4, 'Результат поиска отличается от ожидаемого'


@pytest.mark.asyncio
async def test_get_all_persons(es_client: AsyncElasticsearch, make_get_request, redis_client):
    """
    Тест на вывод всех участников кинопроизведений
    """

    # очистка кеша
    redis = await redis_client
    await redis.flushall()

    persons_count = await es_client.count(body=None, index='persons')

    page_size = 100
    page_number = 1
    data_exists = True
    count_items = 0
    while data_exists:
        response = await make_get_request(
            '/persons/search',
            {'page_size': page_size, 'page_number': page_number, 'sort': 'full_name.raw'},
        )
        count_items += len(response.body)
        data_exists = (response.status == HTTPStatus.OK) and (len(response.body) >= page_size)

        assert response.status == HTTPStatus.OK

        if data_exists:
            page_number += 1
    assert count_items == persons_count['count'], 'Найдены не все данные о людях'


@pytest.mark.asyncio
async def test_search_person_check_redis(
    persons_data, make_get_request, redis_client, make_redis_request
):
    """
    Тест на поиск человека  в кеше Redis
    """

    # очистка кеша
    redis = await redis_client
    await redis.flushall()

    # Заполнение данных для теста
    expected = persons_data[7]

    # # Выполнение запроса через апи
    response = await make_get_request('/persons/' + expected['id'])

    # Проверка результата
    assert response.status == HTTPStatus.OK

    # запрос данных в кеше
    redis_data = await make_redis_request('persons_detail_person_id_' + expected['id'])
    item_from_redis = orjson.loads(redis_data)

    assert item_from_redis == [expected], 'Найденные в кеше данные отличаются от ожидаемых'
