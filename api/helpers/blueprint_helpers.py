from ..user.models import User
from ..extensions import db
import re
from ..exceptions import (
    MissingPasswordData,
    NonStringData,
    PasswordTooLong,
    PasswordTooShort,
    PasswordNotAlphaNumeric,
    UserNameTooLong,
    UserNameTooShort
)
from flask import current_app


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