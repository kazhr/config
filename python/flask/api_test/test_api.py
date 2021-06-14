#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from api import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_health(client):
    rv = client.get("/api/health")
    assert b"ok" in rv.data
