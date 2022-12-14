# -*- coding: utf-8 -*-
"""This module has methods that are used in the other modules in this package."""
import json

from flask import current_app, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from itsdangerous import BadSignature, BadTimeSignature, SignatureExpired

from ..exceptions import (
    EmailAddressTooLong,
    EmptyImageFile,
    EmptyUserData,
    IllegalFileType,
    InvalidEmailAddress,
    InvalidEmailAddressFormat,
    InvalidPassword,
    MissingEmailData,
    MissingEmailKey,
    MissingNameData,
    MissingNameKey,
    MissingPasswordData,
    MissingPasswordKey,
    NonDictionaryUserData,
    PasswordNotAlphaNumeric,
    PasswordTooLong,
    UnActivatedAccount,
    UserDoesNotExist,
    UserExists,
    UserNameTooLong,
    UserNameTooShort,
)
from ..extensions import db, url_serializer
from ..helpers.blueprint_helpers import (
    check_if_email_id_match,
    check_if_user_exists,
    check_if_user_with_id_exists,
    handle_upload_image,
    is_email_address_format_valid,
    is_user_name_valid,
    is_user_password_valid,
)
from ..mail_blueprint.helpers import handle_send_confirm_email
from ..user.models import User, profile_schema, user_schema


def create_new_user(user_data: dict, profile_pic_data) -> dict:
    """Create a new user."""
    if not user_data:
        raise EmptyUserData("The user data cannot be empty.")

    if not isinstance(user_data, dict):
        raise NonDictionaryUserData("user_data must be a dict")

    if "Email" not in user_data.keys():
        raise MissingEmailKey("The email is missing from the user data")

    if not user_data["Email"]:
        raise MissingEmailData("The email data is missing")

    if len(user_data["Email"]) >= current_app.config["EMAIL_MAX_LENGTH"]:
        raise EmailAddressTooLong(
            f'The email address should be less than {current_app.config["EMAIL_MAX_LENGTH"]} characters!'
        )

    if not is_email_address_format_valid(user_data["Email"]):
        raise InvalidEmailAddressFormat("The email address is invalid")

    if "User Name" not in user_data.keys():
        raise MissingNameKey("The name is missing from the user data")

    if not user_data["User Name"]:
        raise MissingNameData("The name data is missing")

    if "Password" not in user_data.keys():
        raise MissingPasswordKey("The password is missing from the user data")

    if not user_data["Password"]:
        raise MissingPasswordData("The password data is missing")

    is_user_name_valid(user_data["User Name"])

    try:
        is_user_password_valid(user_data["Password"])
    except ValueError as e:
        raise e

    if check_if_user_exists(user_data["Email"]):
        raise UserExists(f'The email adress {user_data["Email"]} is already in use.')

    user = User(
        email=user_data["Email"],
        name=user_data["User Name"],
        password=user_data["Password"],
    )

    if profile_pic_data:
        if profile_pic_data["Profile Picture"]:
            profile_pic = handle_upload_image(profile_pic_data["Profile Picture"])
            user.profile_pic = profile_pic

    db.session.add(user)
    db.session.commit()

    return user_schema.dumps(user)


def handle_create_user(request_data: dict, profile_pic):
    """Handle the POST request to the /api/v1/user route."""
    try:
        registered_user_data = create_new_user(request_data, profile_pic)
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
        MissingPasswordData,
        IllegalFileType,
        EmptyImageFile,
    ) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return registered_user_data, 201


def activate_account(email: str):
    """Activate a user account."""
    user = User.query.filter_by(email=email).first()
    user.active = True
    db.session.commit()
    return jsonify({"Email confirmed": email}), 200


def confirm_email(user_id: str, token: str) -> dict:
    """Confrim user account."""
    if not user_id:
        raise ValueError("The user id has to be provided!")
    if not isinstance(user_id, str):
        raise TypeError("The user id has to be a string!")
    if not token:
        raise ValueError("The token has to be provided!")
    if not isinstance(token, str):
        raise TypeError("The token has to be a string!")

    if not check_if_user_with_id_exists(int(user_id)):
        raise UserDoesNotExist(f"The user with id {user_id} does not exist!")

    email = url_serializer.loads(token, salt="somesalt", max_age=60)

    if not check_if_email_id_match(email, int(user_id)):
        raise ValueError(
            f"The id {user_id} and email {email} do not belong to the same user!"
        )

    return activate_account(email)


def handle_email_confirm_request(user_id: str, token: str) -> dict:
    """Handle the GET request to /api/v1/mail/conrfim."""
    try:
        confirm_data = confirm_email(user_id, token)
    except SignatureExpired as e:
        return jsonify({"error": str(e)}), 400
    except BadTimeSignature as e:
        return jsonify({"error": str(e)}), 400
    except (ValueError, TypeError, UserDoesNotExist) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return confirm_data


def log_in_user(user_id: str, user_data: dict):
    """Log in a registered user."""
    if not user_id:
        raise ValueError("The user id has to be provided!")
    if not isinstance(user_id, str):
        raise TypeError("The user id has to be a string")
    if not check_if_user_with_id_exists(int(user_id)):
        raise UserDoesNotExist(f"There is no user with id {user_id}")
    if not user_data:
        raise EmptyUserData("The user data cannot be empty.")

    if not isinstance(user_data, dict):
        raise NonDictionaryUserData("user_data must be a dict")

    if "email" not in user_data.keys():
        raise MissingEmailKey("The email is missing from the admin data")

    if not user_data["email"]:
        raise MissingEmailData("The email data is missing")

    if "password" not in user_data.keys():
        raise MissingPasswordKey("The password is missing from the admin data")

    if not user_data["password"]:
        raise MissingPasswordData("The password data is missing")

    if not check_if_user_exists(user_data["email"]):
        raise UserDoesNotExist(
            f'The user with email {user_data["email"]} does not exist!'
        )

    if not check_if_email_id_match(user_data["email"], int(user_id)):
        raise UserDoesNotExist(
            f'The user with email {user_data["email"]} and id {user_id} does not exist!'
        )

    user = User.query.filter_by(email=user_data["email"]).first()
    if user:
        if user.check_password(user_data["password"]):
            if user.active:
                user_data = {
                    "user profile": json.loads(profile_schema.dumps(user)),
                    "access token": create_access_token(user.id),
                    "refresh token": create_refresh_token(user.id),
                }

                return user_data
            raise UnActivatedAccount("This account has not been activate.")
        raise InvalidPassword("The admin password is invalid!")


def handle_unactivated_account(email: str) -> dict:
    """Send activation email."""
    return handle_send_confirm_email(email)


def handle_log_in_user(user_id: str, user_data: dict) -> dict:
    """Handle a POST request to log in an admin."""
    try:
        data = log_in_user(user_id, user_data)
    except (
        EmptyUserData,
        NonDictionaryUserData,
        MissingEmailKey,
        MissingEmailData,
        MissingPasswordKey,
        MissingPasswordData,
        ValueError,
        UserDoesNotExist,
        InvalidPassword,
    ) as e:
        return jsonify({"error": str(e)}), 400
    except UnActivatedAccount:
        return handle_unactivated_account(user_data["email"])
    else:
        return data, 200


def logout_user(user_id: str) -> dict:
    """Log out a user."""
    if not user_id:
        raise ValueError("The user id must be provided!")
    if not isinstance(user_id, str):
        raise TypeError("The user id must be a string")
    if not check_if_user_with_id_exists(int(user_id)):
        raise UserDoesNotExist(f"The user with id {user_id} does not exist1")

    return jsonify({"success": "user logged out"}), 200


def handle_logout_user(user_id: str) -> dict:
    """Log out a logged in user."""
    try:
        log_out_data = logout_user(user_id)
    except (ValueError, TypeError, UserDoesNotExist) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return log_out_data


def update_password(email: str, password: str):
    """Update the user password."""
    print("got here")
    if check_if_user_exists(email):
        user = User.query.filter_by(email=email).first()
        user.password = password
        db.session.commit()
        return jsonify({"Success": f"Password reset for {email}"}), 200
    raise InvalidEmailAddress(f"The user with the email {email} does not exist!")


def get_user_email(token: str) -> dict:
    """Get a useremail given a token."""
    try:
        email = url_serializer.loads(token, salt="somesalt", max_age=300)
    except SignatureExpired as e:
        raise e
    except BadTimeSignature as e:
        raise e
    except BadSignature as e:
        raise e
    else:
        return email


def reset_user_password(
    user_id: str, activation_token: str, user_passwrd: dict
) -> dict:
    """Reset the user password."""
    if not user_id:
        raise ValueError("The user id has to be provided")
    if not isinstance(user_id, str):
        raise TypeError("The user id has to be a string")
    if not check_if_user_with_id_exists(int(user_id)):
        raise UserDoesNotExist(f"There is no user with id {user_id}!")
    if not activation_token:
        raise ValueError("The activation token must be provided!")
    if not isinstance(activation_token, str):
        raise ValueError("The activation token must be a string!")
    if not user_passwrd:
        raise ValueError("The password must be provided!")
    if not isinstance(user_passwrd, dict):
        raise TypeError("The user password data must be in a dict")
    if "password" not in user_passwrd.keys():
        raise ValueError("The password key must be in the password data!")
    if not user_passwrd["password"]:
        raise ValueError("The new password cannot be empty!")

    email = get_user_email(activation_token)

    if not check_if_email_id_match(email, int(user_id)):
        raise ValueError(
            f"The user id {user_id} and email {email} belong to different users!"
        )

    return update_password(email, user_passwrd["password"])


def handle_reset_password(
    user_id: str, activation_token: str, user_passwrd: dict
) -> dict:
    """Reset user password."""
    try:
        reset = reset_user_password(user_id, activation_token, user_passwrd)
    except (ValueError, TypeError, UserDoesNotExist) as e:
        return jsonify({"error": str(e)})
    except SignatureExpired as e:
        return jsonify({"error": str(e)}), 400
    except BadTimeSignature as e:
        return jsonify({"error": str(e)}), 400
    except BadSignature as e:
        return jsonify({"error": str(e)}), 400
    else:
        return reset


def handle_refresh_token(identity) -> dict:
    """Generate a new access token."""
    return jsonify(access_token=create_access_token(identity=identity)), 200
