from toolz.dicttoolz import get_in

from gcalcli.events.helpers import convert_date, split_by

EVENT_KIND_MAPPING = {
    'calendar#event': 'event'
}


def format_create_event_request(flags):
    return {
        'start': convert_date(flags['start'], to_dict=True),
        'end': convert_date(flags['end'], to_dict=True),
        'status': flags['status'],
        'sendUpdates': flags['send_updates'],
        'summary': flags['summary'],
        'attendees': [
            {'email': mail} for mail in flags['attendees']
        ],
        'reminders': {'userDefault': True}
    }


def format_list_events_request(flags):
    return {
        'timeMin': convert_date(flags['start']),
        'timeMax': convert_date(flags['end']) if flags.get('end') else None,
        'filter': flags['filter'],
        'showDeleted': flags['show_deleted']
    }


def format_single_event(response):
    start = response['start']
    end = response['end']
    return {
        'creator': get_in(['creator', 'displayName'], response),
        'status': response.get('status'),
        'summary': split_by(response.get('summary', '')),
        'start': start.get('date') or start.get('dateTime'),
        'end': end.get('date') or end.get('dateTime'),
        'kind': EVENT_KIND_MAPPING.get(response.get('kind'), 'unknown'),
        'all_day': 'Yes' if response['start'].get('date') else 'No'
    }


def format_events_list_response(response):
    return [format_single_event(e) for e in response]
