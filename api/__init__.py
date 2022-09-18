from flask import Flask, jsonify
from .user.views import user
from .auth.views import auth
from .extensions import cors, db, migrate, ma, swagger, jwt, mail, bcrypt
from .helpers.helpers import set_flask_environment
from flasgger import LazyJSONEncoder
from .mail_blueprint.views import mail as mail_blueprint


def create_app(script_info=None):
    """Create the flask app."""

    app = Flask(__name__)

    set_flask_environment(app)

    @app.route("/", methods=["GET"])
    def health_check():
        """Check if the application is up."""

        return jsonify({"Hello": "From Flask"}), 200

    app.json_encoder = LazyJSONEncoder
    swagger.init_app(app)

    # initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(user, url_prefix="/api/v1/user")
    app.register_blueprint(auth, url_prefix="/api/v1/auth")
    app.register_blueprint(mail_blueprint, url_prefix="/api/v1/mail")

    # shell context for flask cli
    app.shell_context_processor({"app": app})
    return app
