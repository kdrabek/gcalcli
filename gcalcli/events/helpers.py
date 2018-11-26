import click
from textwrap import wrap
from dateparser import parse
from datetime import datetime
import time

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


def is_all_day(d):
    # this is a bit naive approach, because it will fail when someone wants
    # to create an event from midnight to midnight the next day
    return d.hour == 0 and d.minute == 0


def stringify(d, add_timezone=False):
    result = {}

    if is_all_day(d):
        result['date'] = d.strftime("%Y-%m-%d")
    else:
        result['dateTime'] = d.strftime("%Y-%m-%dT%H:%M:%S%z")

    if add_timezone:
        result['timezone'] = d.tzinfo.zone

    return result

def stringify2(d):
    return d.strftime("%Y-%m-%dT%H:%M:%S%z")

def validate_date(value):
    parsed = parse(value, settings={
        'RETURN_AS_TIMEZONE_AWARE': True,
        'PREFER_DAY_OF_MONTH': 'first',
        'DATE_ORDER': 'DMY'
    })
    if parsed is None:
        raise click.BadParameter(value)
    return parsed
