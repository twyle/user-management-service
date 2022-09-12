# -*- coding: utf-8 -*-
"""This module has methods that are used in the other modules in this package."""
import re

from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from flask import current_app
from ..user.models import User, user_schema
from ..extensions import db
from ..exceptions import (
    EmptyUserData,
    NonDictionaryUserData,
    NonStringData,
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
    PasswordTooShort,
    MissingPasswordData,
    UserNameTooShort,
    UserNameTooLong,
)


def is_email_address_format_valid(email_address: str) -> bool:
    """Check that the email address format is valid."""
    if not email_address:
        raise ValueError('The email_address cannot be an empty value')

    if not isinstance(email_address, str):
        raise ValueError('The email_address must be a string')

    #  Regular expression for validating an Email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if re.fullmatch(regex, email_address):
        return True

    return False


def is_user_name_valid(user_name: str) -> bool:
    """Check if the user name is valid."""
    if not user_name:
        raise ValueError('The user_name has to be provided.')

    if not isinstance(user_name, str):
        raise ValueError('The user_name has to be string')

    if len(user_name) >= current_app.config['NAME_MAX_LENGTH']:
        raise UserNameTooLong(f'The user_name has to be less than {current_app.config["NAME_MAX_LENGTH"]}')

    if len(user_name) <= current_app.config["NAME_MIN_LENGTH"]:
        raise UserNameTooShort(f'The user_name has to be more than {current_app.config["NAME_MIN_LENGTH"]}')

    if not user_name.isalnum():
        raise ValueError('The user_name has to be alphanumeric.')

    return True


def is_user_password_valid(user_password: str):
    """Check if the user_password is valid."""
    if not user_password:
        raise MissingPasswordData('The user_password has to be provided.')

    if not isinstance(user_password, str):
        raise NonStringData('The user_password has to be string')

    if len(user_password) >= current_app.config["PASSWORD_MAX_LENGTH"]:
        raise PasswordTooLong(f'The user_password has to be less than {current_app.config["PASSWORD_MAX_LENGTH"]}')

    if len(user_password) <= current_app.config["PASSWORD_MIN_LENGTH"]:
        raise PasswordTooShort(f'The user_password has to be more than {current_app.config["PASSWORD_MIN_LENGTH"]}')

    if user_password.isalnum():
        msg = 'When checking if user_password is valid, he user_password was not alphanumeric.'
        raise PasswordNotAlphaNumeric('The user_password has to be alphanumeric.')

    return True


def check_if_user_exists(user_email: str) -> bool:
    """Check if the admin with the given user_email exists."""
    if not user_email:
        raise ValueError('The user_email has to be provided.')

    if not isinstance(user_email, str):
        raise ValueError('The user_email has to be an integer')

    user = User.query.filter_by(email=user_email).first()

    if user:
        return True

    return False


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
        new_user = create_new_user(request_data)
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
        return new_user, 201
