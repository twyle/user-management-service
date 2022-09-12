from .models import User, user_schema, users_schema
from ..extensions import db
from flask import jsonify
from ..exceptions import (
    EmptyUserData,
    UserDoesNotExist
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