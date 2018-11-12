from datetime import datetime
from os import path
from pprint import pprint

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client, file, tools

SCOPES = 'https://www.googleapis.com/auth/calendar'
BASE_DIR = path.abspath(path.dirname(__file__))

def authorize():
    token_file = path.join(BASE_DIR, 'authorization/token.json')
    credentials_file = path.join(BASE_DIR, 'authorization/credentials.json')

    store = file.Storage(token_file)
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(credentials_file, SCOPES)
        creds = tools.run_flow(flow, store)

    return creds


def get_calendar_client(creds):
    return build('calendar', 'v3', http=creds.authorize(Http()))


def get_events(calendar):
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = calendar.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    return events

def insert_event(calendar):
    example_event = {
    'summary': 'Test',
    'location': '800 Howard St., San Francisco, CA 94103',
    'description': 'Testing inserting events into Google Calendar API',
    'start': {
        'dateTime': '2018-11-12T11:00:00+01:00',
        'timeZone': 'Europe/Warsaw',
    },
    'end': {
        'dateTime': '2018-11-12T12:00:00+01:00',
        'timeZone': 'Europe/Warsaw',
    },
    'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=2'
    ],
    'attendees': [
        {'email': 'kdrabek@gmail.com'}
    ],
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'email', 'minutes': 30},
        {'method': 'popup', 'minutes': 10},
        ],
    },
    }
    calendar.events().insert(calendarId='primary', body=example_event).execute()


def main():
    creds = authorize()
    calendar = get_calendar_client(creds)
    events = get_events(calendar)
    for event in events:
        pprint(event)
    # insert_event(calendar)



if __name__ == '__main__':
    main()
