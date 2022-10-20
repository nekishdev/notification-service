import uuid
from http import HTTPStatus
from typing import List

from typing import Optional
from fastapi import APIRouter, HTTPException, Depends

from providers.genre import get_genre_service
from services.genre import GenreService
from api.v1.schemes import Genre

import api.v1.query_params as q
import api.v1.messages as msg

from pydantic.error_wrappers import ValidationError


router = APIRouter()


@router.get(
    '/search',
    response_model=List[Genre],
    summary='Поиск жанра кинопроизведения с сортировкой и постраничной выдачей результатов',
    description='Поиск выполняется по названию жанра. В некоторых случаях жанр может быть найден при наличии 1-2 опечаток',
    response_description='Метод возвращает список жанров с идентификатором и названием',
)
async def genre_search(
    query: Optional[str] = None,
    sort: Optional[str] = None,
    page_size: Optional[int] = q.page_size,
    page_number: Optional[int] = q.page_number,
    genre_service: GenreService = Depends(get_genre_service),
) -> List[Genre]:
    items, error = await genre_service.search(
        query=query, sort=sort, page_size=page_size, page_number=page_number
    )
    if not items:
        if error and error.status_code == HTTPStatus.BAD_REQUEST:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=error.info)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=msg.GENRES_NOT_FOUND)

    return [Genre(**p.dict()) for p in items]


@router.get(
    '/{genre_id}',
    response_model=Genre,
    summary='Получение жанра кинопроизведения по идентификатору',
    description='Получение жанра кинопроизведения по идентификатору',
    response_description='Метод возвращает жанр с идентификатором и названием',
)
async def genre_detail(
    genre_id: uuid.UUID, genre_service: GenreService = Depends(get_genre_service)
) -> Genre:
    try:
        item = await genre_service.detail(genre_id)
    except ValidationError as error:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=error.json())

    if not item:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=msg.GENRES_NOT_FOUND)

    return Genre(**item.dict())
