# -*- coding: utf-8 -*-
"""This module has exceptions that are used in the other modules in this package."""


class EmptyUserData(Exception):
    """Raised when no user data is provided."""


class NonStringData(Exception):
    """Raised when the data provided is not string."""


class NonDictionaryUserData(Exception):
    """Raised when the user data is not provided in a dictionary."""


class MissingEmailKey(Exception):
    """Raised when the 'email' key is missing in user data."""


class MissingNameKey(Exception):
    """Raised when the 'name' key is missing in user data."""


class MissingPasswordKey(Exception):
    """Raised when the 'password' key is missing in user data."""


class MissingEmailData(Exception):
    """Raised when the email is empty in user data."""


class MissingNameData(Exception):
    """Raised when the name is empty in user data."""


class MissingPasswordData(Exception):
    """Raised when the password is empty in user data."""


class EmailAddressTooLong(Exception):
    """Raised when the provided email address is too long."""


class InvalidEmailAddressFormat(Exception):
    """Raised when the email address format is invalid."""


class UserExists(Exception):
    """Raised when the given user exists."""


class UserDoesNotExist(Exception):
    """Raised when the given user does not exist."""


class PasswordTooLong(Exception):
    """Raised when the given admin password is too long."""
    

class PasswordTooShort(Exception):
    """Raised when the given admin password is too short."""


class PasswordNotAlphaNumeric(Exception):
    """Raised when the given admin password is not alphanumeric."""


class InvalidPassword(Exception):
    """Raised when an invalid admin password is given."""
    

class UserNameTooShort(Exception):
    """Raised when the username given is too short."""


class UserNameTooLong(Exception):
    """Raised when the username given is too long."""
    

class UnActivatedAccount(Exception):
    """Raised when the user attempts to log into a unactivated account."""


class ActivatedAccount(Exception):
    """Raised when the user attempts to activate an activated account."""


class InvalidEmailAddress(Exception):
    """Raised when the email address is invalid."""
    

class EmptyImageFile(Exception):
    """Raised when no image file is given."""


class IllegalFileType(Exception):
    """Raised when an illegal file type is uploaded."""
    
