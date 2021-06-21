#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from pathlib import Path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

base_dir = Path(__file__).resolve().parent
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_service():
    """
    Based on quickstart.py
    (https://github.com/googleworkspace/python-samples/blob/master/gmail/quickstart/quickstart.py)
    """
    creds = None
    token_file = base_dir / "token.json"
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds_file = base_dir / "credentials.json"
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_file), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with token_file.open('w') as fp:
            fp.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def show_recent_messages(after):
    """
    Parameters
    ----------
    after : int
        Unixtime
    """
    service = get_service()

    # Call the Gmail API
    results = service.users().messages().list(userId="me", q=f"after:{int(after)}").execute()
    messages = results.get("messages", [])

    if not messages:
        print("No messages found.")
    else:
        for message in messages:
            print(message)


if __name__ == '__main__':
    after = (datetime.datetime.now() - datetime.timedelta(days=1)).timestamp()
    show_recent_messages(after)
