import pytest
from unittest.mock import MagicMock
from gcalcli.events.api import get_events
from gcalcli.events.helpers import validate_date, stringify2


@pytest.fixture
def mock_client(event_json):
    resp ={'items': [event_json]}
    client = MagicMock()
    client.events.return_value.list.return_value.execute.return_value = resp
    return client


@pytest.fixture
def flags():
    return {
        'timeMin': stringify2(validate_date('01-11-2018')),
        'timeMax': stringify2(validate_date('05-11-2018')),
        'filter': None,
        'showDeleted': True,
    }


def assert_mock_calls(mock_client, expected_count):
    execute = mock_client.events.return_value.list.return_value.execute
    assert execute.call_count == expected_count


def test_get_events(mock_client, event_json, flags):
    events = get_events(mock_client, flags)

    assert [e for e in events] == [event_json]
    assert_mock_calls(mock_client, expected_count=1)


def test_get_events_with_valid_title_filter(mock_client, event_json, flags):
    flags['filter'] = event_json['summary']
    events = get_events(mock_client, flags)

    assert [e for e in events] == [event_json]
    assert_mock_calls(mock_client, expected_count=1)


def test_get_events_with_invalid_title_filter(mock_client, event_json,flags):
    flags['filter'] = 'some title'
    events = get_events(mock_client, flags)

    assert [e for e in events] == []
    assert_mock_calls(mock_client, expected_count=1)


def test_get_events_calls_next_page(mock_client, event_json, flags):
    resp_with_token ={'items': [event_json], 'nextPageToken': 'token'}
    resp = {'items': [event_json]}
    mock_client.events.return_value.list.return_value.execute.side_effect = [
        resp_with_token, resp
    ]

    events = get_events(mock_client, flags)

    assert [e for e in events] == [event_json, event_json]
    assert_mock_calls(mock_client, expected_count=2)
