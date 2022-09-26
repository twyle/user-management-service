# -*- coding: utf-8 -*-
"""Declare the routes used by the mail package."""
from celery.result import AsyncResult
from flasgger import swag_from
from flask import Blueprint, jsonify, request

from .helpers import handle_send_confirm_email, handle_send_reset_password_email

mail = Blueprint("mail", __name__)


@mail.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    """Get the status of a scheduled task."""
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    return jsonify(result), 200


@mail.route("/send_confirm_email", methods=["POST"])
@swag_from("./docs/send.yml", endpoint="mail.send_mail", methods=["POST"])
def send_mail():
    """Send an email."""
    return handle_send_confirm_email(request.args.get("id"), request.json)


@mail.route("/send_reset_password_email", methods=["POST"])
@swag_from(
    "./docs/password_reset.yml", endpoint="mail.reset_password", methods=["POST"]
)
def reset_password():
    """Handle password reset."""
    return handle_send_reset_password_email(request.args.get("id"), request.json)
