from flask import Blueprint, jsonify, request

import services.social_auth as service
from helpers.http import failed, success
from services.abstract_auth_service import AbstractAuthService

auth_router = Blueprint('auth', __name__)


@auth_router.route('/get_link', methods=['GET'])
def get_auth_link():
    """get link on authorization page
    ---
    parameters:
      - name: service_name
        in: body
        required: true
        schema:
           type: object
           properties:
             name:
               type: string
               example: yandex | vk
    responses:
      200:
        description: url for authorization page
    """
    auth_service_name = request.args.get('service_name')

    auth_service: AbstractAuthService = service.auth_service_by_name(auth_service_name)

    if auth_service is None:
        return failed(message='Unknown authorization service name')

    url = auth_service.get_auth_link()

    return jsonify(url=url)


@auth_router.route('/get_token', methods=['GET'])
def get_auth_token():
    """get jwt tokens by authorization code after successful authorization in social network account (yandex, VK)
    ---
    parameters:
      - name: service_name
        in: arguments
        required: true
        schema:
           type: object
           properties:
             name:
               type: string
               example: yandex | vk
      - name: code
        in: arguments
        required: true
        schema:
           type: object
           properties:
             name:
               type: string
               example: 1250214
    responses:
      200:
        description: jwr access and refresh tokens
    """
    auth_service_name = request.args.get('service_name')
    code = request.args.get('code', default=None, type=None)

    return_data = service.process_auth_token(auth_service_name, code, request.headers.get('User-Agent'))

    return success('User logged with social network account', return_data)
