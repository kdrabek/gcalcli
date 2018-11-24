from glom import Coalesce, Call, T
from gcalcli.events.helpers import split_by


EVENT_KIND_MAPPING = {
    'calendar#event': 'event'
}


event = {
    'creator': 'creator.displayName',
    'status': 'status',
    'summary': (Coalesce('summary', default=''), split_by),
    'start': Coalesce('start.date', 'start.dateTime'),
    'end': Coalesce('end.date', 'end.dateTime'),
    'kind': ('kind', lambda e: EVENT_KIND_MAPPING.get(e, 'unknown')),
    'all_day': lambda d: 'Yes' if d['start'].get('date') else 'No'
}
