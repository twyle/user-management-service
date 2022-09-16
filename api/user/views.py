from flask import Blueprint, request
from .helpers import handle_delete_user, handle_get_all_users, handle_get_user, handle_update_user
from flasgger import swag_from
from flask_jwt_extended import jwt_required


user = Blueprint('user', __name__)


@user.route('/', methods=['GET'])
@jwt_required()
@swag_from("./docs/get_user.yml", endpoint='user.get_user', methods=['GET'])
def get_user():
    return handle_get_user(request.args.get('id'))


@user.route('/', methods=['PUT'])
@jwt_required()
@swag_from("./docs/update_user.yml", endpoint='user.update_user', methods=['PUT'])
def update_user():
    return handle_update_user(request.args.get('id'), request.form, request.files)


@user.route('/', methods=['DELETE'])
# @jwt_required()
@swag_from("./docs/delete_user.yml", endpoint='user.delete_user', methods=['DELETE'])
def delete_user():
    """Delete a user."""
    return handle_delete_user(request.args.get('id'))


@user.route('/users', methods=['GET'])
@jwt_required()
@swag_from("./docs/get_all_users.yml", endpoint='user.get_all_users', methods=['GET'])
def get_all_users():
    """List all the registered users."""
    return handle_get_all_users()

