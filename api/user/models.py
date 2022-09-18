from ..extensions import db, ma, bcrypt
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
    password_hash: str = db.Column(db.String(100), nullable=False)
    profile_pic: str = db.Column(db.String(100), nullable=True)
    
        
    @property
    def password(self):
        raise AttributeError('Password is a write-only field!')
    
    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'date_registered', 'active', 'admin', 'profile_pic')
        
        
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