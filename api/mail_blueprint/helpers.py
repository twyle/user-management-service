# -*- coding: utf-8 -*-
"""Declare methods used to send emails."""
from flask import jsonify

from ..exceptions import ActivatedAccount, UnActivatedAccount, UserDoesNotExist
from ..helpers.blueprint_helpers import (
    check_if_email_id_match,
    check_if_user_with_id_exists,
    is_email_address_format_valid,
)
from ..tasks import celery_send_email
from ..user.models import User


def send_confirm_email(user_id: str, email_data: dict) -> dict:
    """Send account confirmation email."""
    if not user_id:
        raise ValueError("The user id must be provided")
    if not isinstance(user_id, str):
        raise TypeError("The user id must be a string")
    if not email_data:
        raise ValueError("The email data cannot be empty")
    if not isinstance(email_data, dict):
        raise TypeError("The email data should be a dict")
    if "email" not in email_data.keys():
        raise ValueError("The email key is missing in email data")
    if not email_data["email"]:
        raise ValueError("The email cannot be empty")
    if not is_email_address_format_valid(email_data["email"]):
        raise ValueError("The email address format is invalid")
    if not check_if_user_with_id_exists(int(user_id)):
        raise UserDoesNotExist(f"The user with id {user_id} does not exist!")
    if not check_if_user_with_email_exists(email_data["email"]):
        raise UserDoesNotExist(
            f'The user with email {email_data["email"]} does not exist!'
        )

    if not check_if_email_id_match(email_data["email"], int(user_id)):
        raise UserDoesNotExist(
            f'There is no user with the id {user_id} and email {email_data["email"]}'
        )

    if check_if_user_active(int(user_id)):
        raise ActivatedAccount("This account has alreadybeen activated!")

    task = celery_send_email.delay(
        user_id, email_data["email"], "Confirm Account", "auth.confirm_email"
    )

    return (
        jsonify(
            {"task_id": task.id, "Confirm Account email sent to": email_data["email"]}
        ),
        202,
    )


def handle_send_confirm_email(user_id: str, email_data: dict) -> dict:
    """Send the confirmation email."""
    try:
        confirm_email_data = send_confirm_email(user_id, email_data)
    except (ValueError, TypeError, UserDoesNotExist, ActivatedAccount) as e:
        return jsonify({"error": str(e)})
    else:
        return confirm_email_data


def check_if_user_with_email_exists(user_email: int) -> bool:
    """Check if the user with the given user_email exists."""
    if not user_email:
        raise ValueError("The user_email has to be provided.")

    if not isinstance(user_email, str):
        raise ValueError("The user_email has to be an string")

    user = User.query.filter_by(email=user_email).first()

    if user:
        return True

    return False


def check_if_user_active(id: int) -> bool:
    """Check if account has been activated."""
    return User.query.filter_by(id=id).first().active


def send_password_reset_email(id: str, email_data: dict) -> dict:
    """Send password reset email."""
    if not id:
        raise ValueError("The user id has to be provided!")

    if not isinstance(id, str):
        raise ValueError("The id has to be a string")

    if not email_data:
        raise ValueError("The email is missing!")

    if not isinstance(email_data, dict):
        raise ValueError("The email data must be a dict")

    if "email" not in email_data.keys():
        raise ValueError("The email has to be provided")

    if not email_data["email"]:
        raise ValueError("The email has to be provided!")

    if not check_if_user_with_id_exists(int(id)):
        raise UserDoesNotExist(f"There is no user with id {id}")

    if not check_if_user_with_email_exists(email_data["email"]):
        raise UserDoesNotExist(f'There is no user with the email {email_data["email"]}')

    if not check_if_email_id_match(email_data["email"], int(id)):
        raise UserDoesNotExist(
            f'There is no user with the id {id} and email {email_data["email"]}'
        )

    if not check_if_user_active(int(id)):
        raise UnActivatedAccount("You cannot change password for unactivated account!")

    task = celery_send_email.delay(
        id, email_data["email"], "Password Reset", "auth.reset_password"
    )

    return (
        jsonify(
            {"task_id": task.id, "Password Reset Email sent to": email_data["email"]}
        ),
        202,
    )


def handle_send_reset_password_email(id: str, email_data: dict) -> dict:
    """Handle request to send reset password email."""
    try:
        email_sent = send_password_reset_email(id, email_data)
    except (ValueError, UserDoesNotExist, UnActivatedAccount) as e:
        return jsonify({"error": str(e)})
    else:
        return email_sent
