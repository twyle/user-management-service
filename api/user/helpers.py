from .models import User, user_schema, users_schema
from ..extensions import db
from flask import jsonify, current_app
from ..helpers.blueprint_helpers import (
    is_email_address_format_valid,
    check_if_user_exists,
    is_user_name_valid
)
from ..exceptions import (
    EmptyUserData,
    UserDoesNotExist,
    NonDictionaryUserData,
    EmailAddressTooLong,
    UserExists,
    UserNameTooShort,
    UserNameTooLong,
    InvalidEmailAddressFormat,
    MissingEmailData,
    MissingPasswordData,
    MissingNameData,
    MissingEmailKey,
    MissingNameKey,
    MissingPasswordKey
)


def check_if_user_with_id_exists(user_id: int) -> bool:
    """Check if the user with the given user_id exists."""
    if not user_id:
        raise ValueError('The user_id has to be provided.')

    if not isinstance(user_id, int):
        raise ValueError('The user_id has to be an integer')

    user = User.query.filter_by(id=user_id).first()

    if user:
        return True

    return False


def delete_user(user_id: str) -> dict:
    """Delete the user with the given id."""
    if not user_id:
        raise EmptyUserData('The user_id has to be provided.')

    if not isinstance(user_id, str):
        raise ValueError('The user_id has to be a string.')
    
    user_id = int(user_id)

    if not check_if_user_with_id_exists(user_id):
        raise UserDoesNotExist(f'The user with id {user_id} does not exist.')

    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()

    return user
    

def handle_delete_user(user_id: int):
    """Handle the DELETE request to the /api/v1/user route."""
    try:
        user = delete_user(user_id)
    except (
        ValueError,
        EmptyUserData,
        UserDoesNotExist
    ) as e:
        return jsonify({'error': str(e)}), 400
    else:
        return user_schema.dumps(user), 200
    

def handle_get_all_users():
    """List all users."""
    all_users = User.query.all()
    return users_schema.dump(all_users), 200


def get_user(user_id: int) -> dict:
    """Get the user with the given id."""
    if not user_id:
        raise EmptyUserData('The user_id has to be provided.')

    if not isinstance(user_id, int):
        raise ValueError('The user_id has to be an integer.')

    if not check_if_user_with_id_exists(user_id):
        raise UserDoesNotExist(f'The user with id {user_id} does not exist.')

    user = User.query.filter_by(id=user_id).first()

    return user_schema.dumps(user)


def handle_get_user(user_id: str):
    """Handle the GET request to the /api/v1/user route."""
    try:
        user = get_user(int(user_id))
    except (
        ValueError,
        EmptyUserData,
        UserDoesNotExist
    ) as e:
        return jsonify({'error': str(e)}), 400
    else:
        return user, 200
    
    
def check_if_user_with_name_exists(user_name: str) -> bool:
    """Check if the User with the given user_name exists."""
    if not user_name:
        raise ValueError('The user_name has to be provided.')

    if not isinstance(user_name, str):
        raise ValueError('The user_name has to be string')

    user = User.query.filter_by(name=user_name).first()

    if user:
        return True

    return False


def update_user(user_id: int, user_data: dict) -> dict:  # pylint: disable=R0912
    """Update the user with the given id."""
    if not user_id:
        raise EmptyUserData('The user_id has to be provided.')

    if not isinstance(user_id, int):
        raise ValueError('The user_id has to be an integer.')

    if not check_if_user_with_id_exists(user_id):
        raise UserDoesNotExist(f'The user with id {user_id} does not exist.')

    if not user_data:
        raise EmptyUserData('The user data cannot be empty.')

    if not isinstance(user_data, dict):
        raise NonDictionaryUserData('user_data must be a dict')

    for key in user_data.keys():
        valid_keys = ['name', 'email', 'profile_pic']
        if key not in valid_keys:
            raise KeyError(f'Invalid key {key}. The valid keys are {valid_keys}.')

    if 'email' in user_data.keys():
        is_email_address_format_valid(user_data['email'])

        if len(user_data['email']) >= current_app.config["EMAIL_MAX_LENGTH"]:
            raise EmailAddressTooLong('The email address is too long')

        if check_if_user_exists(user_data['email']):
            raise UserExists(f'The email adress {user_data["email"]} is already in use.')

    if 'name' in user_data.keys():
        is_user_name_valid(user_data['name'])

    user = User.query.filter_by(id=user_id).first()
    if 'email' in user_data.keys():
        user.email = user_data['email']
    if 'name' in user_data.keys():
        user.name = user_data['name']
    db.session.commit()

    return user_schema.dumps(user)


def handle_update_user(user_id: int, user_data: dict):
    """Handle the GET request to the /api/v1/user route."""
    try:
        user = update_user(user_id, user_data)
    except (
        UserExists,
        InvalidEmailAddressFormat,
        UserNameTooShort,
        UserNameTooLong,
        EmailAddressTooLong,
        MissingPasswordData,
        MissingNameData,
        MissingEmailData,
        NonDictionaryUserData,
        ValueError,
        EmptyUserData,
        UserDoesNotExist
    ) as e:
        return jsonify({'error': str(e)}), 400
    else:
        return user, 200