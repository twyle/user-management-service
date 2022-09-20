from .extensions import celery, s3
from .mail_blueprint.models import EmailMessage
from flask import current_app
from os import path


@celery.task(name="send_email")
def celery_send_email(
    email_address: str, email_title: str, api_email_link: str
) -> dict:
    """Send the reset email."""
    email_message = EmailMessage(
        email_title=email_title,
        api_email_link=api_email_link,
        email_address=email_address, 
    )

    return email_message.send_message()


def delete_file_s3(filename):
    """Delete profile pic"""
    print(path.basename(filename))
    s3.delete_object(
        Bucket=current_app.config["S3_BUCKET"], Key=path.basename(filename)
    )


@celery.task(name="upload_image")
def upload_file_to_s3(file_path, bucket_name):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    with open(file_path, "rb") as file:
        try:
            s3.upload_fileobj(file, bucket_name, path.basename(file.name))
        except Exception as e:
            raise e 
        else:
            data = "{}{}".format(
                current_app.config["S3_LOCATION"], path.basename(file.name)
            )
            return {'image': data}