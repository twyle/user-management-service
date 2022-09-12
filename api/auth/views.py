from flask import Blueprint, jsonify, request
from flasgger import swag_from
from .helpers import handle_create_user


auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
@swag_from("./docs/register_user.yml", endpoint='auth.register', methods=['POST'])
def register():
    """Create a new User."""
    return handle_create_user(request.json)


@auth.route('/login', methods=['POST'])
@swag_from("./docs/login_user.yml", endpoint='auth.login', methods=['POST'])
def login():
    return jsonify({'Hello': 'From the login route!'}), 200


@auth.route('/confirm', methods=['GET'])
@swag_from("./docs/confirm_user.yml", endpoint='auth.confirm', methods=['GET'])
def confirm():
    return jsonify({'Hello': 'From the confirm route!'}), 200


@auth.route('/logout', methods=['POST'])
@swag_from("./docs/logout_user.yml", endpoint='auth.logout', methods=['POST'])
def logout():
    return jsonify({'Hello': 'From the logout route!'}), 200


@auth.route('/refresh', methods=['POST'])
@swag_from("./docs/refresh_token.yml", endpoint='auth.refresh', methods=['POST'])
def refresh():
    return jsonify({'Hello': 'From the refresh-token route!'}), 200