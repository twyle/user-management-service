# -*- coding: utf-8 -*-
"""This module tests the default route."""


def test_health(client):
    """Tests that the default route returns ok message on GET request.

    GIVEN we have the / route
    WHEN we send a GET request
    THEN we should get a 200 OK response
    """
    resp = client.get("/")
    assert resp.status_code == 200
