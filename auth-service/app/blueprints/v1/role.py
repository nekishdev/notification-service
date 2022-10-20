from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import update

from helpers.db import db
from helpers.http import admin_required, failed, success
from models.models import Role

role_router = Blueprint('role', __name__)


@role_router.route('/', methods=['POST'])
@jwt_required()
@admin_required()
def create_role():
    """Create new role. Only for admin user.
    ---
    security:
        - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
           type: object
           properties:
             name:
               type: string
               example: Content manager
    responses:
      200:
        description: Role created
    """
    name = request.json.get('name')
    if not name:
        return failed('name is required')

    exist = Role.query.filter_by(name=name).first()
    if exist:
        return failed('Role already exists')

    role = Role(name=name)

    db.session.add(role)
    db.session.commit()

    return success('Role created', {
        'id': role.id
    })


@role_router.route('/<uuid:role_id>', methods=['GET'])
@jwt_required()
@admin_required()
def retrieve_role(role_id):
    """Retrieve role. Only for admin user.
    ---
    security:
        - Bearer: []
    parameters:
      - name: role_id
        in: path
        required: true
    responses:
      200:
        description: Role retrieved
    """
    role: Role = Role.query.get(role_id)
    if role is None:
        return failed('Role is not exists', 404)

    return success('Role retrieved', {
        'id': role.id,
        'name': role.name
    })


@role_router.route('/<uuid:role_id>', methods=['PUT'])
@jwt_required()
@admin_required()
def update_role(role_id):
    """Update role. Only for admin user.
    ---
    security:
        - Bearer: []
    parameters:
      - name: role_id
        in: path
        required: true
    responses:
      200:
        description: Role updated
    """
    name = request.json.get('name')
    if not name:
        return failed('name is required')

    role: Role = Role.query.get(role_id)
    if role is None:
        return failed('Role is not exists', 404)

    role = Role(id=role.id, name=name)

    db.session.execute(update(Role).where(Role.id == role.id).values(name=name))
    db.session.commit()

    return success('Role updated', {
        'id': role.id,
        'name': role.name
    })


@role_router.route('/<uuid:role_id>', methods=['DELETE'])
@jwt_required()
@admin_required()
def delete_role(role_id):
    """Delete role. Only for admin user.
    ---
    security:
        - Bearer: []
    parameters:
      - name: role_id
        in: path
        required: true
    responses:
      200:
        description: Role deleted
    """
    role = Role.query.get(role_id)
    if role is None:
        return failed('Role is not exists', 404)

    db.session.delete(role)
    db.session.commit()

    return success('Role deleted', {
        'id': role.id
    })
