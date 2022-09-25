# -*- coding: utf-8 -*-
"""Declare the celery tasks."""
import io
import json
from os import path

import numpy as np
from flask import current_app
from PIL import Image

from .extensions import celery, s3
from .mail_blueprint.models import EmailMessage


@celery.task(name="send_email")
def celery_send_email(
    id: str, email_address: str, email_title: str, api_email_link: str
) -> dict:
    """Send the reset email."""
    email_message = EmailMessage(
        user_id=id,
        email_title=email_title,
        api_email_link=api_email_link,
        email_address=email_address,
    )

    return email_message.send_message()


def delete_file_s3(filename):
    """Delete profile pic."""
    print(path.basename(filename))
    s3.delete_object(
        Bucket=current_app.config["S3_BUCKET"], Key=path.basename(filename)
    )


@celery.task(name="upload_image")
def upload_file_to_s3(json_data, filename, bucket_name):
    """Upload a file to S3."""
    img = Image.fromarray(np.array(json.loads(json_data), dtype="uint8"))
    in_mem_file = io.BytesIO()
    img.save(in_mem_file, format="png")
    in_mem_file.seek(0)

    s3.upload_fileobj(in_mem_file, bucket_name, filename)

    data = f"{current_app.config['S3_LOCATION']}{filename}"
    return {"image": data}
