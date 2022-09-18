# -*- coding: utf-8 -*-
"""This module tests the default route."""


def test_development_config(create_development_app):
    assert create_development_app.config['DEBUG'] is True
    assert create_development_app.config['TESTING'] is False
    assert create_development_app.config['SECRET_KEY'] == 'secret-key'