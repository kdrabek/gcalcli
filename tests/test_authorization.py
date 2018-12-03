import json
from unittest.mock import MagicMock, mock_open, patch

import pytest
from google_auth_oauthlib.flow import Flow

from gcalcli.authorization import (
    SCOPES, create_credentials, load_credentials, open_file
)


@pytest.fixture
def open_path():
    return 'gcalcli.authorization.open'


@pytest.fixture
def flow():
    m = MagicMock(spec=Flow)
    m.client_config = {
        'token_uri': 'token_uri',
        'client_id': 'client_id',
        'client_secret': 'client_secret'
    }
    return m


@pytest.fixture
def token_json():
    return {
        'access_token': 'access_token',
        'refresh_token': 'refresh_token'
    }


@pytest.fixture
def mock_mkdir():
    path = 'gcalcli.authorization.Path'
    with patch(path):
        yield


@pytest.fixture
def mock_open_function(token_json):
    path = 'gcalcli.authorization.open'
    mock_content = json.dumps(token_json)

    with patch(path, mock_open(read_data=mock_content)) as m:
        yield m


def assert_credentials(credentials, token_json, flow):
    assert credentials.token == token_json['access_token']
    assert credentials.refresh_token == token_json['refresh_token']
    assert credentials.token_uri == flow.client_config['token_uri']
    assert credentials.client_id == flow.client_config['client_id']
    assert credentials.client_secret == flow.client_config['client_secret']
    assert credentials.scopes == SCOPES


def test_open_file(mock_open_function):
    open_file('/foo/bar')

    mock_open_function.assert_called_once_with('/foo/bar', 'r')


def test_open_file_with_formatter(mock_open_function):
    content = open_file('/foo/bar', formatter=json.loads)

    mock_open_function.assert_called_once_with('/foo/bar', 'r')
    assert isinstance(content, dict)
    assert content['access_token'] == 'access_token'


def test_create_credentials(flow, token_json):
    credentials = create_credentials(token_json, flow, scopes=SCOPES)

    assert_credentials(credentials, token_json, flow)


@patch('gcalcli.authorization.Flow')
def test_load_credentials(
        mock_flow, flow, mock_open_function, mock_mkdir, token_json):
    mock_flow.from_client_secrets_file.return_value = flow
    credentials = load_credentials()

    assert_credentials(credentials, token_json, flow)
