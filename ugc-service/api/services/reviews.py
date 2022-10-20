import typing as t

from uuid import UUID

import pymongo
from exceptions.crud_error import CrudError
from exceptions.permission_error import UserPermissionError
from helpers.mongo import mongo

from models.enums import ScoreValueEnum
from models.review import Review, ReviewScore


def _get_reviews_collection() -> pymongo.collection.Collection:
    return mongo["reviews"]


def add_review(review: Review) -> str:
    doc = review.dict(by_alias=True)
    insert_result = _get_reviews_collection().insert_one(doc)
    return str(insert_result.inserted_id)


def edit_review(_id: UUID, user_id: UUID, values_: dict) -> None:
    if not _check_user_is_author(user_id, _id):
        raise UserPermissionError(user_id, "edit", "review", _id)

    _filter = {"_id": _id}
    update_result = _get_reviews_collection().update_one(_filter, values_)
    if not update_result.acknowledged:
        raise CrudError("update", "review", _id, update_result.raw_result)


def get_review(_id: UUID, *, user_id: t.Optional[UUID] = None) -> t.Optional[Review]:
    _filter = {"_id": _id}
    if user_id:
        _filter["user_id"] = user_id

    doc = _get_reviews_collection().find_one(_filter)
    if not doc:
        return None

    return Review(**doc)


def delete_review(_id: UUID, user_id: UUID) -> None:
    if not _check_user_is_author(user_id, _id):
        raise UserPermissionError(user_id, "delete", "review", _id)

    delete_result = _get_reviews_collection().delete_one({"_id": _id})
    if not delete_result.acknowledged:
        raise CrudError("delete", "review", _id, delete_result.raw_result)


def like_review(_id: UUID, user_id: UUID) -> None:
    _add_score_to_review(_id, user_id, ScoreValueEnum.LIKE)


def dislike_review(_id: UUID, user_id: UUID) -> None:
    _add_score_to_review(_id, user_id, ScoreValueEnum.DISLIKE)


def _add_score_to_review(review_id: UUID, user_id: UUID, score_value: int) -> None:
    existent_score = _get_user_review_score(user_id, review_id, score_value)
    if existent_score:
        return

    score = ReviewScore(user_id=user_id,
                        score_value=score_value)
    _update = {
        "$push": {
            "scores": score.dict()
        }
    }
    update_result = _get_reviews_collection().update_one({"_id": review_id}, _update)
    if not update_result.acknowledged:
        raise CrudError("add_score", "review", review_id, update_result.raw_result)


def _get_user_review_score(user_id: UUID, review_id: UUID, score_value: int) -> ReviewScore:
    projection = {
        "scores": {
            "$elemMatch": {
                "user_id": user_id,
                "value": score_value
            }
        }
    }
    review = _get_reviews_collection().find_one({"_id": review_id}, projection=projection)

    scores = review.get("scores") or []
    if not scores:
        return None

    return ReviewScore(**scores.pop())


def _check_user_is_author(user_id: UUID, review_id: UUID) -> bool:
    return get_review(review_id, user_id=user_id) is not None
