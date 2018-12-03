import click
from textwrap import wrap
from dateparser import parse

from terminaltables import AsciiTable

HEADERS = [
    'CREATOR', 'STATUS', 'SUMMARY', 'START', 'END', 'TYPE', 'ALL DAY?'
]


def to_table(events):
    table_data = [HEADERS]
    table_data.extend([e.values() for e in events])
    return AsciiTable(table_data).table


def split_by(s, len=45):
    return '\n'.join(wrap(s, len))


def convert_date(d, to_dict=False):
    if not to_dict:
        return d.strftime("%Y-%m-%dT%H:%M:%S%z")

    result = {
        'timezone': d.tzinfo.zone
    }

    if d.hour == 0 and d.minute == 0:
        # this is a bit naive approach, because it will fail when someone
        # wants to create an event from midnight to midnight the next day
        result['date'] = d.strftime("%Y-%m-%d")
    else:
        result['dateTime'] = d.strftime("%Y-%m-%dT%H:%M:%S%z")
    return result


def validate_date(ctx, param, value):
    if value is None:
        return

    parsed = parse(value, settings={
        'RETURN_AS_TIMEZONE_AWARE': True,
        'PREFER_DAY_OF_MONTH': 'first',
        'DATE_ORDER': 'DMY'
    })
    if parsed is None:
        raise click.BadParameter(value)
    return parsed
