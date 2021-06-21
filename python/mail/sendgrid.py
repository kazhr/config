#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, From, Subject, Content, MimeType


API_KEY = os.getenv("SENDGRID_API_KEY")

message = Mail()
message.from_email = From(email="shima-kh@itec.hankyu-hanshin.co.jp")
message.to = To(email="itechh.statuspage@gmail.com")
message.subject = Subject("Sending with SendGrid")
message.content = Content(MimeType.text, "Hello!")

sendgrid_client = SendGridAPIClient(API_KEY)
response = sendgrid_client.send(message)
print(response)
