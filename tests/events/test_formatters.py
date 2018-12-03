from datetime import datetime

import pytest
import pytz

from gcalcli.events import formatters


def test_format_create_event():
    timezone = pytz.timezone('Europe/Warsaw')
    flags = {
        'start': datetime(2018, 12, 3, 20, 0, 0, tzinfo=timezone),
        'end': datetime(2018, 12, 3, 21, 0, 0, tzinfo=timezone),
        'status': 'confirmed',
        'send_updates': True,
        'summary': 'test event',
        'attendees': ['test@email.com']
    }
    assert formatters.format_create_event_request(flags) == {
        'start': {
            'dateTime': '2018-12-03T20:00:00+0124',
            'timezone': 'Europe/Warsaw'
        },
        'end': {
            'dateTime': '2018-12-03T21:00:00+0124',
            'timezone': 'Europe/Warsaw'
        },
        'status': flags['status'],
        'sendUpdates': flags['send_updates'],
        'summary': flags['summary'],
        'attendees': [{
            'email': flags['attendees'][0]
        }],
        'reminders': {'userDefault': True}
    }


def test_formats_list_events_request():
    flags = {
        'start': datetime(2018, 12, 3, 20, 0, 0),
        'end': datetime(2018, 12, 3, 21, 0, 0),
        'filter': 'test',
        'show_deleted': True
    }
    assert formatters.format_list_events_request(flags) == {
        'timeMin': '2018-12-03T20:00:00',
        'timeMax': '2018-12-03T21:00:00',
        'filter': flags['filter'],
        'showDeleted': flags['show_deleted']
    }


def test_formats_single_event(event_json):
    assert formatters.format_single_event(event_json) == {
        'all_day': 'No',
        'creator': 'John Smith',
        'end': '2018-11-01T22:00:00+01:00',
        'kind': 'event',
        'start': '2018-11-01T21:00:00+01:00',
        'status': 'tentative',
        'summary': 'Summary'
    }


@pytest.mark.parametrize('payload, result', [
    ({'date': '2018-11-13'}, '2018-11-13'),
    ({'dateTime': '2018-12-19T13:00:00+01:00'}, '2018-12-19T13:00:00+01:00')
])
def test_format_single_event_different_date_fields(
        payload, result, event_json):
    event_json['start'] = payload
    event_json['end'] = payload

    formatted = formatters.format_single_event(event_json)

    assert formatted['start'] == result
    assert formatted['end'] == result


def test_format_event_list(event_json):
    assert formatters.format_events_list_response([event_json]) == [{
        'all_day': 'No',
        'creator': 'John Smith',
        'end': '2018-11-01T22:00:00+01:00',
        'kind': 'event',
        'start': '2018-11-01T21:00:00+01:00',
        'status': 'tentative',
        'summary': 'Summary'
    }]
