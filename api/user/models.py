from email.policy import default
from ..extensions import db, ma
from datetime import datetime
from dataclasses import dataclass


@dataclass
class User(db.Model):
    """A user.
    
    """
    
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    email: str = db.Column(db.Text, nullable=False)
    date_registered = db.Column(db.DateTime(), default=datetime.utcnow)
    active: bool = db.Column(db.Boolean(), nullable=False, default=False)
    admin: bool = db.Column(db.Boolean(), nullable=False, default=False)
    password: str = db.Column(db.String(100), nullable=False)
    profile_pic: str = db.Column(db.String(100), nullable=True)

    def __init__(self, name: str, email: str, password: str) -> None:
        """Create a new user.
        
        Creates a new user in the user table with an increasing id, with active
        set as True by default and with the given email.
        
        Attributes
        ----------
        email: str
            The user's email
        """
        self.name = name
        self.email = email 
        self.password = password


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'date_registered')
        
        
class ProfileSchema(ma.Schema):
    class Meta:
        fields = ('name', 'email', 'profile_pic')
        
class AuthSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'date_registered', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)
profile_schema = ProfileSchema()
auth_schema = AuthSchema()