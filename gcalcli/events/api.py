PRIMARY_CALENDAR_ID = 'primary'


def get_events(client, opts):
    title_filter = opts.pop('filter')
    page_token = None
    while True:
        opts['pageToken'] = page_token
        events = client.events().list(
            calendarId=PRIMARY_CALENDAR_ID, **opts).execute()
        if not events:
            return []

        for event in events['items']:
            summary = event.get('summary', '').lower()
            if title_filter and title_filter.lower() not in summary:
                continue

            yield event

        page_token = events.get('nextPageToken')
        if not page_token:
            break


def create_event(client, opts):
    opts['calendarId'] = PRIMARY_CALENDAR_ID
    try:
        event = client.events().insert(
            calendarId=PRIMARY_CALENDAR_ID, body=opts).execute()
    except Exception as e:
        print("Exception occurred", e)
        return None
    else:
        return event
