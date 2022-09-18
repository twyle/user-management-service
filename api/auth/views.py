from flask import Blueprint, jsonify, request
from flasgger import swag_from
from .helpers import (
    handle_create_user,
    handle_log_in_user,
    handle_reset_password,
    handle_refresh_token,
    handle_logout_user,
    handle_email_confirm_request
)
from flask_jwt_extended import jwt_required, get_jwt_identity


auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
@swag_from("./docs/register_user.yml", endpoint='auth.register', methods=['POST'])
def register():
    """Create a new User."""
    return handle_create_user(request.form, request.files)


@auth.route('/confirm_email', methods=['GET'])
@swag_from("./docs/confirm.yml", endpoint='auth.confirm_email', methods=['GET'])
def confirm_email():
    """Handle email confirmation."""
    return handle_email_confirm_request(request.args.get('id'), request.args.get('token'))


@auth.route('/login', methods=['POST'])
@swag_from("./docs/login_user.yml", endpoint='auth.login', methods=['POST'])
def login():
    return handle_log_in_user(request.args.get('id'), request.json)


@auth.route('/logout', methods=['POST'])
# @jwt_required()
@swag_from("./docs/logout_user.yml", endpoint='auth.logout', methods=['POST'])
def logout():
    # nullify the access token
    return handle_logout_user(request.args.get('id'))


@auth.route('/refresh_token', methods=['POST'])
# @jwt_required(refresh=True)
@swag_from("./docs/refresh_token.yml", endpoint='auth.refresh', methods=['POST'])
def refresh():
    """Generate a refresh token."""
    return handle_refresh_token(get_jwt_identity())


@auth.route('/reset_password', methods=['POST'])
@swag_from("./docs/password_reset.yml", endpoint='auth.reset_password', methods=['POST'])
def reset_password():
    return handle_reset_password(request.args.get('id'), request.args.get('token'), request.json)