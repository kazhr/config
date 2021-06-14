#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sendgrid
import os
from flask import Flask, jsonify
from sendgrid.helpers.mail import Mail, Email, Content, Personalization


app = Flask(__name__)
sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))


def post(request_body):
    """
    Wrapping the SendGrid mail sending method in order to patch it while testing.
    (https://github.com/sendgrid/sendgrid-python/issues/293)
    """
    return sg.client.mail.send.post(request_body=request_body)


@app.route("/api/mail/send")
def mail_send():

    from_email = Email("from@example.com")
    content = Content("text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, plain_text_content=content)

    personalization = Personalization()
    personalization.subject = "Sending with SendGrid is Fun"
    for i in range(2):
        to_email = Email(f"to{i}@example.com")
        personalization.add_to(to_email)
    mail.add_personalization(personalization)

    response = post(mail.get())

    data = {
        "status_code": response.status_code,
    }
    return jsonify(data)
