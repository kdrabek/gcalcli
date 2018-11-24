import pytest

from click import exceptions

from gcalcli.events.helpers import split_by, to_table, validate_date


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
    result = validate_date(None, 'start','January 2018')
    assert result == '2018-01-01T00:00:00+0000'


def test_validate_date_unknown_lang():
    with pytest.raises(exceptions.BadParameter):
        result = validate_date(None, 'start','abcd xyz')


def test_validate_date_incorrect_date():
    with pytest.raises(exceptions.BadParameter):
        result = validate_date(None, 'start','32 Nov 2018')
