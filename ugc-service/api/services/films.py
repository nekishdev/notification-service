import uuid

import pymongo
from exceptions.crud_error import CrudError
from exceptions.not_found import NotFoundError
from helpers.mongo import mongo

from models import enums
from models.film import Film, FilmScore


def _get_film_score_collection() -> pymongo.collection.Collection:
    return mongo["film_scores"]


def _get_film_collection() -> pymongo.collection.Collection:
    return mongo["films"]


def _ensure_film_exists(film_id: uuid.UUID) -> Film:
    doc = _get_film_collection().find_one({"_id": film_id})
    if doc:
        return Film(**doc)
    else:
        doc = Film(_id=film_id)
        _get_film_collection().insert_one(doc.dict(by_alias=True))
        return doc


def _increase_film_counters(film: Film, score_value: int) -> None:
    film.score_count += 1
    if score_value == enums.ScoreValueEnum.LIKE:
        film.like_count += 1
    elif score_value == enums.ScoreValueEnum.DISLIKE:
        film.dislike_count += 1

    film.avg_score = (film.avg_score + score_value) / film.score_count

    values_ = {"$set": film.dict(exclude={"id": True})}
    update_result = _get_film_collection().update_one({"_id": film.id}, values_)
    if not update_result.acknowledged:
        raise CrudError("update", "film", film.id, update_result.raw_result)


def add_score(score: FilmScore) -> str:
    insert_result = _get_film_score_collection().insert_one(score.dict())
    film = _ensure_film_exists(score.film_id)
    _increase_film_counters(film, score.score_value)

    return str(insert_result.inserted_id)


def get_film_scores(film_id: uuid.UUID) -> dict:
    doc: dict = _get_film_collection().find_one({"_id": film_id})
    if not doc:
        raise NotFoundError("film", film_id)

    return doc
