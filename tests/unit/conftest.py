# -*- coding: utf-8 -*-
"""This module sets up the fixtures that will be used in our testing."""
import pytest
from api import create_app as create_app_, db
from api.config.config import (
    DevelopmentConfig,
    ProductionConfig,
    StagingConfig,
    TestingConfig,
)


@pytest.fixture
def create_app():
    """Create the app instance."""
    return create_app_()


@pytest.fixture
def create_db():
    """Create the db instance."""
    return db


@pytest.fixture
def client():
    """Create the test client."""
    create_app_().config.from_object(TestingConfig)
    test_client = create_app_().test_client()
    with create_app_().app_context():
        db.drop_all()
        db.create_all()

    return test_client


@pytest.fixture
def create_test_app():
    """Create the test client with the test config."""
    create_app_().config.from_object(TestingConfig)
    return create_app_()


@pytest.fixture
def create_development_app():
    """Create the test client with the development config."""
    create_app_().config.from_object(DevelopmentConfig)
    return create_app_()


@pytest.fixture
def create_staging_app():
    """Create the test client with the staging config."""
    create_app_().config.from_object(StagingConfig)
    return create_app_()


@pytest.fixture
def create_production_app():
    """Create the test client with the production config."""
    create_app_().config.from_object(ProductionConfig)
    return create_app_()
