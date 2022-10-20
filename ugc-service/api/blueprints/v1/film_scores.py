from uuid import UUID

from flask import Blueprint, Response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from helpers.http import success

import services.films as film_services
from models.film import FilmScore

film_score_router = Blueprint('film_score', __name__)


@film_score_router.route('/<uuid:film_id>', methods=['POST'])
@jwt_required()
def add_score(film_id: UUID) -> Response:
    """Add score for film.
    ---
    security:
        - Bearer: []
    tags:
        - Film scores
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
            value: 5
    responses:
      200:
        description: Score saved
    """
    user_id = UUID(get_jwt_identity())
    value_ = request.json.get("value")
    if value_ is None:
        raise ValueError("body.value is required")

    value_ = int(value_)
    score = FilmScore(user_id=user_id, film_id=film_id, score_value=value_)

    film_services.add_score(score)
    return success('Score saved')


@film_score_router.route('/<uuid:film_id>', methods=['GET'])
def get_film_scores(film_id: UUID) -> Response:
    """Get film scores.
    ---
    security:
        - Bearer: []
    tags:
        - Film scores
    parameters:
      - name: film_id
        in: path
        required: true
        schema:
           type: uuid
    responses:
      200:
        description: Film scores retrieved
    """
    # user_id = UUID(get_jwt_identity())

    film = film_services.get_film_scores(film_id)
    return success('Film retrieved', film)
