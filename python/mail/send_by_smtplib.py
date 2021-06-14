#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import smtplib
from email.message import EmailMessage


content = """\
Hello!!
This is a test mail.
"""

msg = EmailMessage()
msg.set_content(content)

msg["Subject"] = "Test"
msg["From"] = "me@localhost"
msg["To"] = "to@example.com"

s = smtplib.SMTP("localhost:1025")
s.send_message(msg)
