import uuid
from http import HTTPStatus
from typing import Optional, List

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi_jwt_auth import AuthJWT

from providers.film import get_film_service
from services.film import FilmService
from api.v1.schemes import Film
import api.v1.query_params as q
import api.v1.messages as msg

router = APIRouter()


@router.get(
    '/',
    response_model=List[Film],
    summary='Поиск кинопроизведений с возможностью фильтрации по жанру, сортировкой и постраничной выдачей результатов',
    description='Поиск кинопроизведений с возможностью фильтрации по жанру',
    response_description='Метод возвращает название, рейтинг фильма, описание, жанр и участников',
)
async def film_list(
    sort: Optional[str] = None,
    page_size: Optional[int] = q.page_size,
    page_number: Optional[int] = q.page_number,
    genre: Optional[uuid.UUID] = Query(
        None, alias='filter[genre]', description='Filter by genre id',
    ),
    film_service: FilmService = Depends(get_film_service),
) -> List[Film]:
    films = await film_service.get_list(
        sort=sort, page_size=page_size, page_number=page_number, genre_id=genre
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=msg.FILMS_NOT_FOUND)

    return [Film(**film.dict()) for film in films]


@router.get(
    '/search',
    response_model=List[Film],
    summary='Поиск кинопроизведений с сортировкой и постраничной выдачей результатов',
    description='Полнотекстовый поиск кинопроизведений названию, описанию, участникам',
    response_description='Метод возвращает список кинопроизведений с названием, рейтингом, описанием, жанром и участниками',
)
async def film_search(
    query: str,
    sort: Optional[str] = None,
    page_size: Optional[int] = q.page_size,
    page_number: Optional[int] = q.page_number,
    film_service: FilmService = Depends(get_film_service),
) -> List[Film]:
    films = await film_service.search(
        query=query, sort=sort, page_size=page_size, page_number=page_number
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=msg.FILMS_NOT_FOUND)

    return [Film(**film.dict()) for film in films]


@router.get(
    '/new',
    response_model=List[Film],
    summary='Получение новинок кинопроизведений',
    description='Получение последний вышедших кинопроизведений. Доступно только авторизованному пользователю.',
    response_description='Метод возвращает название, рейтинг фильма, описание, жанр и участников',
)
async def films_new(
        page_size: Optional[int] = q.page_size,
        page_number: Optional[int] = q.page_number,
        jwt: AuthJWT = Depends(),
        film_service: FilmService = Depends(get_film_service)
) -> List[Film]:
    jwt.jwt_required()
    films = await film_service.search(
        query='new', sort='-imdb_rating', page_size=page_size, page_number=page_number
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=msg.FILMS_NOT_FOUND)

    return [Film(**film.dict()) for film in films]


@router.get(
    '/{film_id}',
    response_model=Film,
    summary='Получение кинопроизведения по идентификатору',
    description='Получение кинопроизведения по идентификатору',
    response_description='Метод возвращает название, рейтинг фильма, описание, жанр и участников',
)
async def film_details(
    film_id: uuid.UUID, film_service: FilmService = Depends(get_film_service)
) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=msg.FILMS_NOT_FOUND)

    return Film(**film.dict())
