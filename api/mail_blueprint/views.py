from flask import Blueprint, request
from .helpers import (
    handle_email_confirm_request,
    handle_send_confirm_email,
    handle_send_reset_password_email
)
from flasgger import swag_from


mail = Blueprint('mail', __name__)

@mail.route('/send_confirm_email', methods=['POST'])
@swag_from("./docs/send.yml", endpoint='mail.send_mail', methods=['POST'])
def send_mail():
    """Send an email"""    
    return handle_send_confirm_email(request.json['email'])

@mail.route('/confirm_email', methods=['GET'])
@swag_from("./docs/confirm.yml", endpoint='mail.confirm_email', methods=['GET'])
def confirm_email():
    """Handle email confirmation."""
    return handle_email_confirm_request(request.args.get('token'))


@mail.route('/send_reset_password_email', methods=['POST'])
@swag_from("./docs/password_reset.yml", endpoint='mail.reset_password', methods=['POST'])
def reset_password():
    #generate new access token
    return handle_send_reset_password_email(request.args.get('id'), request.json)