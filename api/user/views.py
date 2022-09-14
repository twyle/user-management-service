from flask import Blueprint, jsonify, request
from .helpers import handle_delete_user, handle_get_all_users, handle_get_user, handle_update_user
from flasgger import swag_from


user = Blueprint('user', __name__)


@user.route('/', methods=['GET'])
@swag_from("./docs/get_user.yml", endpoint='user.get_user', methods=['GET'])
def get_user():
    return handle_get_user(request.args.get('id'))


@user.route('/', methods=['PUT'])
@swag_from("./docs/update_user.yml", endpoint='user.update_user', methods=['PUT'])
def update_user():
    return handle_update_user(request.args.get('id'), request.json)


@user.route('/', methods=['DELETE'])
@swag_from("./docs/delete_user.yml", endpoint='user.delete_user', methods=['DELETE'])
def delete_user():
    """Delete a user."""
    return handle_delete_user(request.args.get('id'))


@user.route('/users', methods=['GET'])
@swag_from("./docs/get_all_users.yml", endpoint='user.get_all_users', methods=['GET'])
def get_all_users():
    """List all the registered users."""
    return handle_get_all_users()

