from gcalcli.cal import SCOPES

def test_is_sane():
    assert 1+1 == 2

def test_is_possible_to_import_from_project():
    assert SCOPES == 'https://www.googleapis.com/auth/calendar'
