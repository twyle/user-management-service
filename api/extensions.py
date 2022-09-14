from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flasgger import LazyString, Swagger
from flask import request
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
import os


cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
mail = Mail()
url_serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY', 'secret-key'))


swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "User Management System.",
        "description": "An application for managing user registration, authentication and authorization.",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "email": "lyceokoth@gmail.com",
            "url": "www.twitter.com/lylethedesigner",
        },
        "termsOfService": "www.twitter.com/deve",
        "version": "1.0"
    },
    "host": LazyString(lambda: request.host),
    "basePath": "/",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "APIKeyHeader": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example:\"Authorization: Bearer {token}\""
        }
    },
}


swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(template=swagger_template,
                  config=swagger_config)