import pytest

from click import exceptions
from datetime import datetime
import pytz

from gcalcli.events.helpers import (
    split_by, to_table, validate_date, convert_date
)


@pytest.mark.parametrize('string,result', [
    (
        'very long string above split limit',
        'very long\nstring above\nsplit limit'
    ),
    ('below limit', 'below limit')
])
def test_split_by(string, result):
    assert split_by(string, len=15) == result


def test_to_table_when_no_parsed_event(ascii_table_headers_only):
    parsed_event = []
    result = to_table(parsed_event)
    assert result == ascii_table_headers_only


def test_to_table(parsed_event, ascii_table):
    result = to_table([parsed_event])
    assert result == ascii_table


def test_validate_date():
    result = validate_date({}, 'start', 'January 2018')
    assert isinstance(result, datetime)
    assert str(result) == '2018-01-01 00:00:00+00:00'


def test_validate_date_unknown_lang():
    with pytest.raises(exceptions.BadParameter):
        result = validate_date({}, 'start', 'abcd xyz')


def test_validate_date_incorrect_date():
    with pytest.raises(exceptions.BadParameter):
        result = validate_date({}, 'start', '32 Nov 2018')


def test_convert_date_to_string():
    timezone = pytz.timezone('Europe/Warsaw')
    test_date = datetime(2018, 12, 3, 20, 0, 0)
    assert convert_date(test_date) == '2018-12-03T20:00:00'


def test_convert_date_to_dict_whole_day_events():
    timezone = pytz.timezone('Europe/Warsaw')
    test_date = datetime(2018, 12, 3, 0, 0, 0, tzinfo=timezone)
    assert convert_date(test_date, to_dict=True) == {
        'date': '2018-12-03', 'timezone': 'Europe/Warsaw'
    }


def test_convert_date_to_dict():
    timezone = pytz.timezone('Europe/Warsaw')
    test_date = datetime(2018, 12, 3, 20, 0, 0, tzinfo=timezone)
    assert convert_date(test_date, to_dict=True) == {
        'dateTime': '2018-12-03T20:00:00+0124', 'timezone': 'Europe/Warsaw'
    }