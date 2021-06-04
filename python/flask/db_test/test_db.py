#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import tempfile
import pytest
from sql import create_app, db


@pytest.fixture
def client():
    app = create_app()

    # テスト用のDBを上書き
    db_fd, db_fn = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_fn}"

    # テスト有効化
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            # テスト用DB初期化
            db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(db_fn)


def create_test_user(client):
    return client.post("/create", data=dict(
        username="test",
        mailaddr="test@localhost",
    ), follow_redirects=True)


def test_db(client):
    rv = create_test_user(client)
    assert b"already exists!" not in rv.data

    rv = create_test_user(client)
    assert b"already exists!" in rv.data
