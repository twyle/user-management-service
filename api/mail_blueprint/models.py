# -*- coding: utf-8 -*-
"""Create the models used by the email package."""
from flask import url_for
from flask_mail import Message

from ..extensions import mail, url_serializer


class EmailMessage:
    """Model of the email to be sent."""

    user_id: str
    email_title: str
    email_link: str
    email_address: str
    toke: str

    def __init__(
        self, user_id: str, email_title: str, api_email_link: str, email_address: str
    ) -> None:
        """Create an email message."""
        self.user_id = (user_id,)
        self.email_title = email_title
        self.email_address = email_address
        self.api_email_link = api_email_link

        self._create_token()
        self._create_link()
        self._create_message()

    def _create_token(self):
        """Create the token."""
        self.token = url_serializer.dumps(self.email_address, salt="somesalt")

    def _create_link(self):
        """Create the email link."""
        self.link = url_for(
            self.api_email_link, id=self.user_id, token=self.token, _external=True
        )

    def _create_message(self):
        """Create the email."""
        self.message = Message(
            self.email_title, sender=self.email_address, recipients=[self.email_address]
        )
        self.message.body = f"Your {self.email_title} link is {self.link}"

    def send_message(self):
        """Send the email."""
        mail.send(self.message)
        return {
            f"{self.email_title} email sent to": self.email_address,
            "token": self.token,
        }
