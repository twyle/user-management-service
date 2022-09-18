from ..user.models import User
from ..extensions import db, s3
import re
from ..exceptions import (
    MissingPasswordData,
    NonStringData,
    PasswordTooLong,
    PasswordTooShort,
    PasswordNotAlphaNumeric,
    UserNameTooLong,
    UserNameTooShort,
    EmptyImageFile,
    IllegalFileType,
)
from flask import current_app
from os import path
from werkzeug.utils import secure_filename


def check_if_user_with_id_exists(user_id: int) -> bool:
    """Check if the user with the given user_id exists."""
    if not user_id:
        raise ValueError("The user_id has to be provided.")

    if not isinstance(user_id, int):
        raise ValueError("The user_id has to be an integer")

    user = User.query.filter_by(id=user_id).first()

    if user:
        return True

    return False


def check_if_email_id_match(email: str, id: int) -> bool:
    """Check if user id and email belong to same user"""
    if not id:
        raise ValueError("The user id has to be provided!")

    if not isinstance(id, int):
        raise ValueError("The id has to be an int")

    if not email:
        raise ValueError("The email has to be provided.")

    if not isinstance(email, str):
        raise ValueError("The user_email has to be an string")

    user = User.query.filter_by(id=id).first()

    if user.email == email:
        return True

    return False


def delete_file_s3(filename):
    """Delete profile pic"""
    print(path.basename(filename))
    s3.delete_object(
        Bucket=current_app.config["S3_BUCKET"], Key=path.basename(filename)
    )


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
            return data


def allowed_file(filename: str) -> bool:
    """Check if the file is allowed."""
    allowed_extensions = current_app.config["ALLOWED_EXTENSIONS"]
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def save_file(file):
    """Saves the file locally"""
    filename = secure_filename(file.filename)
    file.save(path.join(current_app.config["UPLOAD_FOLDER"], filename))
    file_path = path.join(current_app.config["UPLOAD_FOLDER"], filename)

    return file_path


def upload_image(file):
    """Uploads image to S3"""
    if not file:
        raise EmptyImageFile("The file has to be provided!")
    if file.filename == "":
        raise EmptyImageFile("The file has to be provided!")
    if not allowed_file(file.filename):
        raise IllegalFileType("That file type is not allowed!")

    file_path = save_file(file)

    profile_pic = upload_file_to_s3(file_path, current_app.config["S3_BUCKET"])

    return profile_pic


def handle_upload_image(file):
    """Handle image upload."""
    try:
        profile_pic = upload_image(file)
        print(profile_pic)
    except (EmptyImageFile, IllegalFileType, ValueError, TypeError) as e:
        raise e
    except Exception as e:
        raise e
    else:
        return profile_pic


def is_user_password_valid(user_password: str):
    """Check if the user_password is valid."""
    if not user_password:
        raise MissingPasswordData("The user_password has to be provided.")

    if not isinstance(user_password, str):
        raise NonStringData("The user_password has to be string")

    if len(user_password) >= current_app.config["PASSWORD_MAX_LENGTH"]:
        raise PasswordTooLong(
            f'The user_password has to be less than {current_app.config["PASSWORD_MAX_LENGTH"]}'
        )

    if len(user_password) <= current_app.config["PASSWORD_MIN_LENGTH"]:
        raise PasswordTooShort(
            f'The user_password has to be more than {current_app.config["PASSWORD_MIN_LENGTH"]}'
        )

    if not user_password.isalnum():
        raise PasswordNotAlphaNumeric("The user_password has to be alphanumeric.")

    return True


def check_if_user_exists(user_email: str) -> bool:
    """Check if the admin with the given user_email exists."""
    if not user_email:
        raise ValueError("The user_email has to be provided.")

    if not isinstance(user_email, str):
        raise ValueError("The user_email has to be an integer")

    user = User.query.filter_by(email=user_email).first()

    if user:
        return True

    return False


def is_email_address_format_valid(email_address: str) -> bool:
    """Check that the email address format is valid."""
    if not email_address:
        raise ValueError("The email_address cannot be an empty value")

    if not isinstance(email_address, str):
        raise ValueError("The email_address must be a string")

    #  Regular expression for validating an Email
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    if re.fullmatch(regex, email_address):
        return True

    return False


def is_user_name_valid(user_name: str) -> bool:
    """Check if the user name is valid."""
    if not user_name:
        raise ValueError("The user_name has to be provided.")

    if not isinstance(user_name, str):
        raise ValueError("The user_name has to be string")

    if len(user_name) >= current_app.config["NAME_MAX_LENGTH"]:
        raise UserNameTooLong(
            f'The user_name has to be less than {current_app.config["NAME_MAX_LENGTH"]}'
        )

    if len(user_name) <= current_app.config["NAME_MIN_LENGTH"]:
        raise UserNameTooShort(
            f'The user_name has to be more than {current_app.config["NAME_MIN_LENGTH"]}'
        )

    return True
