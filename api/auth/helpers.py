# -*- coding: utf-8 -*-
"""This module has methods that are used in the other modules in this package."""
from ..helpers.blueprint_helpers import (
    is_email_address_format_valid,
    check_if_user_exists,
    is_user_name_valid,
    is_user_password_valid
) 
import requests
import json
from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from flask import current_app
from ..user.models import User, user_schema, profile_schema
from ..extensions import db, url_serializer
from ..mail_blueprint.helpers import handle_send_confirm_email
from itsdangerous import SignatureExpired, BadTimeSignature
from ..exceptions import (
    EmptyUserData,
    NonDictionaryUserData,
    MissingEmailKey,
    MissingNameKey,
    MissingPasswordKey,
    EmailAddressTooLong,
    InvalidEmailAddressFormat,
    UserExists,
    MissingEmailData,
    MissingNameData,
    PasswordNotAlphaNumeric,
    PasswordTooLong,
    MissingPasswordData,
    UserNameTooShort,
    UserNameTooLong,
    UserDoesNotExist,
    InvalidPassword,
    UnActivatedAccount,
    InvalidEmailAddress
)


def send_verification_email(emai: str):
    """Send the account verification email"""
    data = {'email': emai}
    url = current_app.config['EMAIL_SERVICE']
    res = requests.post(url=url, json=data)
    
    return res


def create_new_user(user_data: dict) -> dict:  # pylint: disable=R0912
    """Create a new user."""
    if not user_data:
        raise EmptyUserData('The user data cannot be empty.')

    if not isinstance(user_data, dict):
        raise NonDictionaryUserData('user_data must be a dict')

    if 'email' not in user_data.keys():
        raise MissingEmailKey('The email is missing from the user data')

    if not user_data['email']:
        raise MissingEmailData('The email data is missing')

    if len(user_data['email']) >= current_app.config['EMAIL_MAX_LENGTH']:
        raise EmailAddressTooLong(f'The email address should be less than {current_app.config["EMAIL_MAX_LENGTH"]} characters!')

    if not is_email_address_format_valid(user_data['email']):
        raise InvalidEmailAddressFormat('The email address is invalid')

    if 'name' not in user_data.keys():
        raise MissingNameKey('The name is missing from the user data')

    if not user_data['name']:
        raise MissingNameData('The name data is missing')

    if 'password' not in user_data.keys():
        raise MissingPasswordKey('The password is missing from the user data')

    if not user_data['password']:
        raise MissingPasswordData('The password data is missing')

    is_user_name_valid(user_data['name'])

    try:
        is_user_password_valid(user_data['password'])
    except ValueError as e:
        raise e

    if check_if_user_exists(user_data['email']):
        raise UserExists(f'The email adress {user_data["email"]} is already in use.')
    

    user = User(email=user_data['email'], name=user_data['name'],
                  password=user_data['password'])

    db.session.add(user)
    db.session.commit()
    
    return user_schema.dumps(user)


def handle_create_user(request_data: dict):
    """Handle the POST request to the /api/v1/user route."""
    try:
        registered_user_data = create_new_user(request_data)
    except (
        EmptyUserData,
        NonDictionaryUserData,
        MissingEmailKey,
        MissingNameKey,
        MissingPasswordKey,
        EmailAddressTooLong,
        InvalidEmailAddressFormat,
        UserExists,
        MissingEmailData,
        MissingNameData,
        PasswordNotAlphaNumeric,
        PasswordTooLong,
        UserNameTooShort,
        UserNameTooLong,
        MissingPasswordData
    ) as e:
        return jsonify({'error': str(e)}), 400
    else:
        return registered_user_data, 201
    
    
def check_user_password(user_password: str, user: User) -> bool:
    """Check if user passwords match."""
    if user_password == user.password:
        return True
    return False

    
def log_in_user(user_data: dict):
    """Log in a registered user."""
    if not user_data:
        raise EmptyUserData('The user data cannot be empty.')

    if not isinstance(user_data, dict):
        raise NonDictionaryUserData('user_data must be a dict')

    if 'email' not in user_data.keys():
        raise MissingEmailKey('The email is missing from the admin data')

    if not user_data['email']:
        raise MissingEmailData('The email data is missing')

    if 'password' not in user_data.keys():
        raise MissingPasswordKey('The password is missing from the admin data')

    if not user_data['password']:
        raise MissingPasswordData('The password data is missing')

    if check_if_user_exists(user_data['email']):
        user = User.query.filter_by(email=user_data['email']).first()
        if user:
            if check_user_password(user_data['password'], user):
                if user.active:
                    user_data = {
                        'user profile': json.loads(profile_schema.dumps(user)),
                        'access token': create_access_token(user.id),
                        'refresh token': create_refresh_token(user.id)
                    }

                    return user_data
                raise UnActivatedAccount('This account has not been activate.')
            raise InvalidPassword('The admin password is invalid!')
    raise UserDoesNotExist(f'The user with email {user_data["email"]} does not exist!')


def handle_unactivated_account(email: str) -> dict:
    """Sends activation email."""
    return handle_send_confirm_email(email)


def handle_log_in_user(user_data: dict) -> dict:
    """Handle a POST request to log in an admin."""
    try:
        data = log_in_user(user_data)
    except (
        EmptyUserData,
        NonDictionaryUserData,
        MissingEmailKey,
        MissingEmailData,
        MissingPasswordKey,
        MissingPasswordData,
        ValueError,
        UserDoesNotExist
    ) as e:
        return jsonify({'error': str(e)}), 400
    except UnActivatedAccount:
        return handle_unactivated_account(user_data['email'])
    else:
        return data, 200
    

def update_password(email: str, password:str):
    """Updates the user password."""
    print('got here')
    if check_if_user_exists(email):
        user = User.query.filter_by(email=email).first()
        user.password = password
        db.session.commit()
        return jsonify({'Success': f'Password reset for {email}'}), 200
    else:
        raise InvalidEmailAddress(f'The user with the email {email} does not exist!')
        

def get_user_email(token: str) -> dict:
    """Get a useremail given a token."""
    try:
        email = url_serializer.loads(token, salt='somesalt', max_age=300)
    except SignatureExpired as e:
        return jsonify({'error': 'The token has expired!'})
    except BadTimeSignature as e:
        return jsonify({'error': 'Invalid token'})
    else:    
        return email

    
def reset_user_password(activation_token: str, user_passwrd: dict) -> dict:
    """Reset the user password"""
    if not activation_token:
        raise ValueError('The activation token must be provided!')
    if not isinstance(activation_token, str):
        raise ValueError('The activation token must be a string!')
    if not user_passwrd:
        raise ValueError('The passwordmust be provided!')
    if not isinstance(user_passwrd, dict):
        raise TypeError('The user password data must be in a dict')
    if not 'password' in user_passwrd.keys():
        raise ValueError('The password key must be in the password data!')
    if not user_passwrd['password']:
        raise ValueError('The new password cannot be empty!')
    
    email = get_user_email(activation_token)
    
    return update_password(email, user_passwrd['password'])
    

def handle_reset_password(activation_token: str, user_passwrd: dict) -> dict:
    """Reset user password."""
    try:
        reset = reset_user_password(activation_token, user_passwrd)
    except (
        ValueError,
        TypeError
    ) as e:
        return jsonify({'error': str(e)})
    else:
        return reset