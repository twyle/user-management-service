from flask import Blueprint, jsonify


user = Blueprint('user', __name__)


@user.route('/user/<id>', methods=['GET'])
def get_user(id):
    """Get a single user with given id."""
    return jsonify({'user': 'User One!'}), 200