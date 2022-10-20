from flask import Blueprint, request

from blueprints.v1.film import film_router
from blueprints.v1.film_scores import film_score_router
from blueprints.v1.reviews import review_router
from helpers.http import abort


v1_router = Blueprint('v1', __name__)
v1_router.register_blueprint(film_router, url_prefix='/film')
v1_router.register_blueprint(film_score_router, url_prefix='/film-score')
v1_router.register_blueprint(review_router, url_prefix='/review')

# @v1_router.before_request
# def before_request():
#     request_id = request.headers.get('X-Request-Id')
#     if not request_id:
#         return abort(400, 'X-Request-Id header is empty')

