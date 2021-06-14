#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import pytest
import smtplib
from email.message import EmailMessage
from requests.models import Response

from api import app


def post(request_body):
    """
    sendgrid差し替え用
    """

    msg = EmailMessage()
    msg.set_content(request_body["content"][0]["value"])

    msg["Subject"] = request_body["personalizations"][0]["subject"]
    msg["From"] = request_body["from"]["email"]
    msg["To"] = ",".join([to["email"] for to in request_body["personalizations"][0]["to"]])

    s = smtplib.SMTP("localhost:1025")
    s.send_message(msg)

    r = Response()
    r.status_code = 200

    return r


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client, monkeypatch):

    monkeypatch.setattr("api.post", post)

    rv = client.get("/api/mail/send")
    rd = rv.data.decode().strip()
    rj = json.loads(rd)
    assert rj.get("status_code") == 200
