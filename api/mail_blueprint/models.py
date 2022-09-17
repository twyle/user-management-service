from ..extensions import url_serializer, mail
from flask import url_for, jsonify
from flask_mail import Message


class EmailMessage:
    email_title : str
    email_link: str
    email_address: str
    toke: str
    
    def __init__(self, email_title: str, api_email_link: str, email_address: str) -> None:
        """Create an email message"""
        self.email_title = email_title
        self.email_address = email_address
        self.api_email_link = api_email_link
        
        self._create_token()
        self._create_link()
        self._create_message()
        
    def _create_token(self):
        """Creates the token"""
        self.token = url_serializer.dumps(self.email_address, salt='somesalt')
    
    def _create_link(self):
        """Creates the email link"""
        self.link = url_for('mail.confirm_email', token=self.token, _external=True)
        
    def _create_message(self):
        """Create the email"""
        self.message = Message(
            self.email_title, 
            sender=self.email_address, 
            recipients=[self.email_address]
        )
        self.message.body = f'Your {self.email_title} link is {self.link}'
    
    def send_message(self):
        """Send the email"""
        mail.send(self.message)
        return jsonify({f'{self.email_title} email sent to': self.email_address, "token": self.token}), 200