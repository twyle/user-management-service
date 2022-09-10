from flask import Flask, jsonify
from .user.views import user


def create_app(script_info=None):
    """Create the flask app."""
    
    app = Flask(__name__)
    
    @app.route('/', methods=['GET'])
    def health_check():
        """Check if the application is up."""
        
        return jsonify({'Hello': 'From Flask'}), 200
    
    app.register_blueprint(user, url_prefix='/api/v1/')
    
    # shell context for flask cli
    app.shell_context_processor({'app': app})
    return app