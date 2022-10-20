from datetime import datetime
from uuid import UUID

from flask import Blueprint, Response
from flask_jwt_extended import get_jwt_identity, jwt_required
from helpers.http import success
from settings import settings

import services.providers as providers

film_router = Blueprint('film', __name__)


@film_router.route('/<uuid:film_id>/frame', methods=['POST'])
@jwt_required()
def frame(film_id: UUID) -> Response:
    """Add new frame for user and film.
    ---
    security:
        - Bearer: []
    tags:
        - Films
    parameters:
      - name: film_id
        in: path
        required: true
        schema:
           type: uuid
    responses:
      200:
        description: Frame saved
    """
    frame_ts = int(round(datetime.now().timestamp()))
    user_id = get_jwt_identity()
    key = f"{user_id}+{film_id}"

    bus = providers.get_event_bus()
    bus.send(topic=settings.KAFKA_TOPIC_VIEWS,
             msg_value=str(frame_ts),
             key=key)

    return success('Frame saved')
