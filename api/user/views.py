from flask import Blueprint, jsonify
from .models import User, user_schema, users_schema, profile_schema, auth_schema
from flasgger import swag_from


user = Blueprint('user', __name__)


@user.route('/', methods=['GET'])
@swag_from("./docs/get_user.yml", endpoint='user.get_user', methods=['GET'])
def get_user():
    return jsonify({'Hello': 'From the get user route'}), 200


@user.route('/', methods=['PUT'])
@swag_from("./docs/update_user.yml", endpoint='user.update_user', methods=['PUT'])
def update_user():
    return jsonify({'Hello': 'From the update user route'}), 200


@user.route('/', methods=['POST'])
@swag_from("./docs/delete_user.yml", endpoint='user.delete_user', methods=['POST'])
def delete_user():
    return jsonify({'Hello': 'From the delete user route'}), 200


@user.route('/users', methods=['GET'])
@swag_from("./docs/get_all_users.yml", endpoint='user.get_all_users', methods=['GET'])
def get_all_users():
    # all_users = Article.query.all()
    # serialized_articles = articles_schema.dump(all_articles)
    # return jsonify(serialized_articles), 200
    return jsonify({'Hello': 'From the get all users route'}), 200

