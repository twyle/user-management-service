from ..extensions import url_serializer, mail, db
from flask_mail import Message
from itsdangerous import SignatureExpired, BadTimeSignature
from flask import jsonify, url_for
from ..user.models import User
from ..exceptions import InvalidEmailAddress, UserDoesNotExist
from ..helpers.blueprint_helpers import check_if_user_exists
from ..user.helpers import check_if_user_with_id_exists


def activate_account(email: str):
    """Activate a user account."""
    if check_if_user_exists(email):
        user = User.query.filter_by(email=email).first()
        user.active = True
        db.session.commit()
        return
    else:
        raise InvalidEmailAddress(f'The user with the email {email} does not exist!')
        

def handle_email_confirm_request(token: str) -> dict:
    """Handle the GET request to /api/v1/mail/conrfim."""
    try:
        email = url_serializer.loads(token, salt='somesalt', max_age=60)
    except SignatureExpired as e:
        return jsonify({'error': 'The token has expired!'})
    except BadTimeSignature as e:
        return jsonify({'error': 'Invalid token'})
    else:    
        try:
            activate_account(email)
        except InvalidEmailAddress as e:
            return jsonify({'error': str(e)})
        else:
            return jsonify({'Email confirmed': email}), 200
    

def handle_send_confirm_email(email: str) -> dict:
    """Send the confirmation email."""
    token = url_serializer.dumps(email, salt='somesalt')
    link = url_for('mail.confirm_email', token=token, _external=True)
    
    message = Message(
        'Confirm email', 
        sender=email, 
        recipients=['lyceokoth@gmail.com']
        )
    message.body = f'Your link is {link}'
    
    mail.send(message)
    
    return jsonify({'Confirmation email sent to': email, "token": token}), 200


def check_if_user_with_email_exists(user_email: int) -> bool:
    """Check if the user with the given user_email exists."""
    if not user_email:
        raise ValueError('The user_email has to be provided.')

    if not isinstance(user_email, str):
        raise ValueError('The user_email has to be an string')

    user = User.query.filter_by(email=user_email).first()

    if user:
        return True

    return False


def check_if_email_id_match(email: str, id: int) -> bool:
    """Check if user id and email belong to same user"""
    if not id:
        raise ValueError("The user id has to be provided!")
    
    if not isinstance(id, int):
        raise ValueError('The id has to be an int')
    
    if not email:
        raise ValueError('The email has to be provided.')

    if not isinstance(email, str):
        raise ValueError('The user_email has to be an string')
    
    user = User.query.filter_by(id=id).first()
    
    if user.email == email:
        return True
    
    return False


def handle_send_email(email: str) -> dict:
    """Send the reset email."""
    token = url_serializer.dumps(email, salt='somesalt')
    link = url_for('auth.reset_password', token=token, _external=True)
    
    message = Message(
        'Password reset', 
        sender=email, 
        recipients=[email]
        )
    message.body = f'Your password reset is {link}'
    
    mail.send(message)
    
    return jsonify({'Password reset email sent to': email, "token": token}), 200


def send_password_reset_email(id: str, email_data: dict) -> dict:
    """Send password reset email."""
    if not id:
        raise ValueError("The user id has to be provided!")
    
    if not isinstance(id, str):
        raise ValueError('The id has to be a string')
    
    if not email_data:
        raise ValueError('The email is missing!')
    
    if not isinstance(email_data, dict):
        raise ValueError('The email data must be a dict')
    
    if not 'email' in email_data.keys():
        raise ValueError('The email has to be provided')
    
    if not email_data['email']:
        raise ValueError('The email has to be provided!')
    
    if not check_if_user_with_id_exists(int(id)):
        raise UserDoesNotExist(f'There is no user with id {id}')
    
    if not check_if_user_with_email_exists(email_data["email"]):
        raise UserDoesNotExist(f'There is no user with the email {email_data["email"]}')
    
    if not check_if_email_id_match(email_data["email"], int(id)):
        raise UserDoesNotExist(f'There is no user with the id {id} and email {email_data["email"]}')
    
    return handle_send_email(email_data['email'])


def handle_send_reset_password_email(id: str, email_data: dict) -> dict:
    """Handle request to send reset password email"""
    try:
        email_sent = send_password_reset_email(id, email_data)
    except (
        ValueError,
        UserDoesNotExist
    ) as e:
        return jsonify({'error': str(e)})
    else:
        return email_sent