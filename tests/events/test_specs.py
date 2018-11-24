import pytest

from glom import glom
from gcalcli.events import specs


def test_event_parse_result(event_json):
    assert glom(event_json, specs.event) == {
        'all_day': 'No',
        'creator': 'John Smith',
        'end': '2018-11-01T22:00:00+01:00',
        'kind': 'event',
        'start': '2018-11-01T21:00:00+01:00',
        'status': 'tentative',
        'summary': 'Summary'
    }


@pytest.mark.parametrize('payload, result', [
    ({'date': '2018-11-13'}, '2018-11-13'),
    ({'dateTime': '2018-12-19T13:00:00+01:00'}, '2018-12-19T13:00:00+01:00')
])
def test_event_parse_result_dates(payload, result, event_json):
    event_json['start'] = payload
    event_json['end'] = payload

    parsed = glom(event_json, specs.event)

    assert parsed['start'] == result
    assert parsed['end'] == result
