from flask import Blueprint, request
from .helpers import handle_email_confirm_request, handle_send_confirm_email
from flasgger import swag_from


mail = Blueprint('mail', __name__)

@mail.route('/send', methods=['POST'])
@swag_from("./docs/send.yml", endpoint='mail.send_mail', methods=['POST'])
def send_mail():
    """Send an email"""
    email = request.json['email']
    
    return handle_send_confirm_email(email)

@mail.route('/confirm', methods=['GET'])
@swag_from("./docs/confirm.yml", endpoint='mail.confirm_email', methods=['GET'])
def confirm_email():
    """Handle email confirmation."""
    return handle_email_confirm_request(request.args.get('token'))