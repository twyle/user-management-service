# -*- coding: utf-8 -*-
"""Declare helper functions for the application."""
import os

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
        if os.environ["FLASK_ENV"] == "production":  # pragma: no cover
            app.config.from_object("api.config.config.ProductionConfig")
        elif os.environ["FLASK_ENV"] == "development":  # pragma: no cover
            app.config.from_object("api.config.config.DevelopmentConfig")
        elif os.environ["FLASK_ENV"] == "test":
            app.config.from_object("api.config.config.TestingConfig")
        elif os.environ["FLASK_ENV"] == "stage":
            app.config.from_object("api.config.config.StagingConfig")
    except KeyError:
        app.config.from_object("api.config.config.DevelopmentConfig")
        print("Using default values")
        return "development"

    return os.environ["FLASK_ENV"]


def create_db_():
    """Create the database and all the tables."""
    db.drop_all()
    db.create_all()
    db.session.commit()
