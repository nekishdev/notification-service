from uuid import UUID

from flask import Blueprint, Response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from helpers.http import abort, success

import services.reviews as review_services
from models.review import Review

review_router = Blueprint('review', __name__)


@review_router.route('/<uuid:film_id>/review', methods=['POST'])
@jwt_required()
def add_review(film_id: UUID) -> Response:
    """Add new review for film.
    ---
    security:
        - Bearer: []
    tags:
        - Reviews
    parameters:
      - name: film_id
        in: path
        required: true
        schema:
           type: uuid
      - name: body
        in: body
        required: true
        example:
            text: Very good film
    responses:
      200:
        description: Review saved
    """
    user_id = get_jwt_identity()

    review = Review(
        user_id=user_id,
        film_id=film_id,
        text=request.json["text"],
        scores=[]
    )

    _id = review_services.add_review(review)

    return success('Review saved', {"_id": _id})


@review_router.route('/<uuid:review_id>', methods=['PUT'])
@jwt_required()
def edit_review(review_id: UUID) -> Response:
    """Edit existing review.
    ---
    security:
        - Bearer: []
    tags:
        - Reviews
    parameters:
      - name: review_id
        in: path
        required: true
        schema:
           type: uuid
      - name: body
        in: body
        required: true
        example:
            text: Very good film
    responses:
      200:
        description: Review edited
    """
    user_id = get_jwt_identity()

    values_ = {"text": request.json["text"]}

    review_services.edit_review(review_id, user_id, values_)

    return success('Review edited')


@review_router.route('/<uuid:review_id>', methods=['GET'])
def get_review(review_id: UUID) -> Response:
    """Get existing review by id.
    ---
    security:
        - Bearer: []
    tags:
        - Reviews
    parameters:
      - name: review_id
        in: path
        required: true
        schema:
           type: uuid
    responses:
      200:
        description: Review retrieved
    """
    review = review_services.get_review(review_id)
    if not review:
        return abort(404, "Review not found")

    return success('Review retrieved', review.dict())


@review_router.route('/<uuid:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id: UUID) -> Response:
    """Delete existing review by id.
    ---
    security:
        - Bearer: []
    tags:
        - Reviews
    parameters:
      - name: review_id
        in: path
        required: true
        schema:
           type: uuid
    responses:
      200:
        description: Review deleted
    """
    user_id = get_jwt_identity()

    review_services.delete_review(review_id, user_id)

    return success('Review deleted')


@review_router.route('/<uuid:review_id>/like', methods=['POST'])
@jwt_required()
def add_like(review_id: UUID) -> Response:
    """Add like for review. Repeating has no effect.
    ---
    security:
        - Bearer: []
    tags:
        - Reviews
    parameters:
      - name: review_id
        in: path
        required: true
        schema:
           type: uuid
    responses:
      200:
        description: Like saved
    """
    user_id = UUID(get_jwt_identity())
    review_services.like_review(review_id, user_id)
    return success('Like saved')


@review_router.route('/<uuid:review_id>/dislike', methods=['POST'])
@jwt_required()
def add_dislike(review_id: UUID) -> Response:
    """Add dislike for review. Repeating has no effect.
    ---
    security:
        - Bearer: []
    tags:
        - Reviews
    parameters:
      - name: review_id
        in: path
        required: true
        schema:
           type: uuid
    responses:
      200:
        description: Dislike saved
    """
    user_id = get_jwt_identity()
    review_services.like_review(review_id, user_id)
    return success('Dislike saved')
