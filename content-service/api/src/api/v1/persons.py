import uuid
from http import HTTPStatus
from typing import Optional, List

from fastapi import APIRouter, HTTPException, Depends

from providers.person import get_person_service
from providers.film import get_film_service
from services.person import PersonService
from services.film import FilmService
from api.v1.schemes import Film, Person
import api.v1.query_params as q
import api.v1.messages as msg


router = APIRouter()


@router.get(
    '/search',
    response_model=List[Person],
    summary='Поиск участников кинопроизведений с сортировкой и постраничной выдачей результатов',
    description='Поиск участников кинопроизведений по полному имени, допустимы 1-2 опечатки',
    response_description='Метод возвращает список участников кинопроизведений с идентификатором и полным именем',
)
async def person_search(
    query: Optional[str] = None,
    sort: Optional[str] = None,
    page_size: Optional[int] = q.page_size,
    page_number: Optional[int] = q.page_number,
    person_service: PersonService = Depends(get_person_service),
) -> List[Person]:
    items, error = await person_service.search(
        query=query, sort=sort, page_size=page_size, page_number=page_number
    )
    if not items:
        if error and error.status_code == HTTPStatus.BAD_REQUEST:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=error.info)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=msg.PERSONS_NOT_FOUND)

    return [Person(**p.dict()) for p in items]


@router.get(
    '/{person_id}',
    response_model=Person,
    summary='Получение участника кинопроизведения по идентификатору',
    description='Получение участника кинопроизведения по идентификатору',
    response_description='Метод возвращает участника кинопроизведения с идентификатором и полным именем',
)
async def person_detail(
    person_id: uuid.UUID, person_service: PersonService = Depends(get_person_service)
) -> Person:
    item = await person_service.detail(person_id)
    if not item:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=msg.PERSONS_NOT_FOUND)

    return Person(**item.dict())


@router.get(
    '/{person_id}/film',
    response_model=List[Film],
    summary='Поиск фильмов с участием конкретного человека',
    description='Поиск выполняется по идентификатору участника',
    response_description='Метод возвращает список фильмов с идентификатором, названием, описанием, рейтингом, жанром и участниками',
)
async def person_films(
    person_id: uuid.UUID,
    sort: Optional[str] = None,
    page_size: Optional[int] = q.page_size,
    page_number: Optional[int] = q.page_number,
    film_service: FilmService = Depends(get_film_service),
) -> List[Film]:
    items = await film_service.get_list(
        person_id=person_id, sort=sort, page_size=page_size, page_number=page_number
    )
    if not items:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')

    return [Film(**f.dict()) for f in items]
