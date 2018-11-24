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


def validate_date(ctx, param, value):
    try:
        parsed = parse(value, settings={
            'RETURN_AS_TIMEZONE_AWARE': True,
            'PREFER_DAY_OF_MONTH': 'first',
            'DATE_ORDER': 'DMY'
        })
        return parsed.strftime("%Y-%m-%dT%H:%M:%S%z")
    except (ValueError, AttributeError):
        # value error -> unknown lang
        # attribute error -> parse returns None (cannot parse)
        raise click.BadParameter(value)
