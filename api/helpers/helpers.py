import os
from ..user.models import User
from ..extensions import db


def set_flask_environment(app) -> str:
    """Set the flask development environment.
    Parameters
    ----------
    app: flask.Flask
        The flask application object
    Raises
    ------
    KeyError
        If the FLASK_ENV environment variable is not set.
    Returns
    -------
    str:
        Flask operating environment i.e development
    """
    try:
        if os.environ['FLASK_ENV'] == 'production':  # pragma: no cover
            app.config.from_object('api.config.config.ProductionConfig')
        elif os.environ['FLASK_ENV'] == 'development':  # pragma: no cover
            app.config.from_object('api.config.config.DevelopmentConfig')
        elif os.environ['FLASK_ENV'] == 'test':
            app.config.from_object('api.config.config.TestingConfig')
        elif os.environ['FLASK_ENV'] == 'stage':
            app.config.from_object('api.config.config.StagingConfig')
    except KeyError:
        app.config.from_object('api.config.config.DevelopmentConfig')
        print('Using default values')
        return 'development'

    return os.environ['FLASK_ENV']


def seed_db_():
    """Creates two users and on admin."""
    
    lyle_user = User(
        email='lyleuser@gmail.com',
        password='Lyleuser@123',
        name='lyleuser'
    )
    
    lyle_user1 = User(
        email='lyleuser1@gmail.com',
        password='Lyleuse1r@123',
        name='lyleuser1'
    )
    
    lyle_admin = User(
        email='lyleadmin@gmail.com',
        password='Lyleadmin@123',
        name='lyleadmin'
    )
    
    db.session.add_all([lyle_user, lyle_user1, lyle_admin])
    db.session.commit()
    
def create_db_():
    """Create the database and all the tables."""
    db.drop_all()
    db.create_all()
    db.session.commit()
