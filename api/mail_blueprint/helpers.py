from api.auth.helpers import check_if_user_exists
from ..extensions import url_serializer, mail, db
from flask_mail import Message
from itsdangerous import SignatureExpired, BadTimeSignature
from flask import jsonify, url_for
from ..user.models import User
from ..user.helpers import check_if_user_exists
from ..exceptions import InvalidEmailAddress


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