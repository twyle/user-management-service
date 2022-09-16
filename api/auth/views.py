from flask import Blueprint, jsonify, request
from flasgger import swag_from
from .helpers import handle_create_user, handle_log_in_user, handle_reset_password


auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
@swag_from("./docs/register_user.yml", endpoint='auth.register', methods=['POST'])
def register():
    """Create a new User."""
    print(request.form.keys())
    return handle_create_user(request.form)


@auth.route('/login', methods=['POST'])
@swag_from("./docs/login_user.yml", endpoint='auth.login', methods=['POST'])
def login():
    return handle_log_in_user(request.json)


@auth.route('/logout', methods=['POST'])
@swag_from("./docs/logout_user.yml", endpoint='auth.logout', methods=['POST'])
def logout():
    # nullify the access token
    return jsonify({'Hello': 'From the logout route!'}), 200


@auth.route('/refresh_token', methods=['POST'])
@swag_from("./docs/refresh_token.yml", endpoint='auth.refresh', methods=['POST'])
def refresh():
    #generate new access token
    return jsonify({'Hello': 'From the refresh-token route!'}), 200


@auth.route('/reset_password', methods=['POST'])
@swag_from("./docs/password_reset.yml", endpoint='auth.reset_password', methods=['POST'])
def reset_password():
    return handle_reset_password(request.args.get('token'), request.json)