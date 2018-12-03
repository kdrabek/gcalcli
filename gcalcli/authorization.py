import json
from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

# set of permissions for particular API
SCOPES = 'https://www.googleapis.com/auth/calendar'
CONFIG_PATH = Path.home() / '.gcalcli'
CREDENTIALS_PATH = CONFIG_PATH / 'credentials.json'
TOKEN_PATH = CONFIG_PATH / 'token.json'


def open_file(path, formatter=None):
    with open(path, 'r') as f:
        if formatter:
            return formatter(f.read())
        return f.read()


def save_file(path, content):
    with open(path, 'w') as f:
        return f.write(content)


def create_credentials(token, flow, scopes=SCOPES):
    return Credentials(
        token['access_token'],
        refresh_token=token['refresh_token'],
        token_uri=flow.client_config['token_uri'],
        client_id=flow.client_config['client_id'],
        client_secret=flow.client_config['client_secret'],
        scopes=scopes
    )


def setup_authentication():
    Path.mkdir(CONFIG_PATH, exist_ok=True)

    print('Please go to Google API console,')
    print('then generate & download credentials .json file')
    creds = input("Paste contents of the file here: ")

    save_file(CREDENTIALS_PATH, creds)

    flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH, SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    )
    auth_url, _ = flow.authorization_url()

    print('Please go to this URL: {}'.format(auth_url))
    code = input('Enter the authorization code: ')

    token = flow.fetch_token(code=code)
    save_file(TOKEN_PATH, json.dumps(token))

    return create_credentials(token, flow)


def is_authentication_setup():
    Path.mkdir(CONFIG_PATH, exist_ok=True)

    try:
        token = open_file(CREDENTIALS_PATH, json.loads)
        credentials = open_file(TOKEN_PATH)
    except Exception as e:
        print(e)
        return False

    return token is not None and credentials is not None


def load_credentials():
    Path.mkdir(CONFIG_PATH, exist_ok=True)
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH, SCOPES,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob')
    token = open_file(TOKEN_PATH, formatter=json.loads)
    return create_credentials(token, flow)
