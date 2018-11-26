from gcalcli.events.helpers import split_by, stringify, validate_date
from toolz.dicttoolz import get_in


EVENT_KIND_MAPPING = {
    'calendar#event': 'event'
}


def parse_events_list(events):
    return [
        {
            'creator': get_in(['creator', 'displayName'], event),
            'status': event.get('status'),
            'summary': split_by(event.get('summary', '')),
            'start': event['start'].get('date') or event['start'].get('dateTime'),
            'end': event['end'].get('date') or event['end'].get('dateTime'),
            'kind': EVENT_KIND_MAPPING.get(event.get('kind'), 'unknown'),
            'all_day': 'Yes' if event['start'].get('date') else 'No'
        } for event in events
    ]


def serialize_create_event(event):
    return {
        'start': event['start'],
        'end': event['end'],
        'status': event['status'],
        'sendUpdates': event['sendUpdates'],
        'summary': event['summary'],
        'attendees': [{'email': e} for e in event['attendees']],
        'reminders': {'userDefault': True}
    }
