from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

CREDENTIAL_FILE = os.getenv("GOOGLE_CREDS_PATH", "credentials.json")
TOKEN_FILE = os.getenv("TOKEN_PATH", "token.json")


def authentical_google_sheets():
    creds = None

    if os.path.exists(TOKEN_FILE):
        cred = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIAL_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return creds
