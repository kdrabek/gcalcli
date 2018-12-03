import pytest

from terminaltables import AsciiTable

from gcalcli.events.helpers import HEADERS


@pytest.fixture
def event_json():
    return {
        'attendees': [{
            'displayName': 'John Smith',
            'email': 'email@email.com',
            'organizer': True,
            'responseStatus': 'accepted',
            'self': True
        }],
        'created': '2018-11-02T16:53:34.000Z',
        'creator': {
            'displayName': 'John Smith',
            'email': 'email@email.com',
            'self': True
        },
        'end': {'dateTime': '2018-11-01T22:00:00+01:00'},
        'etag': '"2724486429534000"',
        'extendedProperties': {
            'shared': {
                'CalendarSyncAdapter#originalTimezone': 'Europe/Warsaw'
            }
        },
        'htmlLink': 'https://www.google.com/calendar/event?eid=123456',
        'iCalUID': 'icalID@google.com',
        'id': 'some-id',
        'kind': 'calendar#event',
        'organizer': {
            'displayName': 'John Smith',
            'email': 'email@email.com',
            'self': True
        },
        'reminders': {'useDefault': True},
        'sequence': 1,
        'start': {'dateTime': '2018-11-01T21:00:00+01:00'},
        'status': 'tentative',
        'summary': 'Summary',
        'updated': '2018-11-02T16:53:34.767Z'
    }


@pytest.fixture
def parsed_event():
    return {
        'creator': 'John Smith',
        'status': 'tentative',
        'summary': 'Summary',
        'start': '2018-11-01T21:00:00+01:00',
        'end': '2018-11-01T22:00:00+01:00',
        'kind': 'event',
        'all_day': 'No'
    }


@pytest.fixture
def ascii_table_headers_only():
    return AsciiTable([HEADERS]).table


@pytest.fixture
def ascii_table(parsed_event):
    return AsciiTable([HEADERS, parsed_event.values()]).table
