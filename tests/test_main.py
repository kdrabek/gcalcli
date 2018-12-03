import pytest

from click.testing import CliRunner
from unittest.mock import patch
from gcalcli.main import configure, main, ls


@pytest.fixture
def runner():
    return CliRunner()


@patch('gcalcli.main.build')
@patch('gcalcli.main.load_credentials')
@patch('gcalcli.main.is_authentication_setup')
def test_main_when_all_setup(mock_is_setup, mock_load, mock_build, runner):
    result = runner.invoke(main, ['ls'])

    assert result.exit_code == 2
    mock_load.assert_called_once_with()
    mock_build.assert_called_once_with(
        'calendar', 'v3', credentials=mock_load.return_value
    )


@patch('gcalcli.main.build')
@patch('gcalcli.main.load_credentials')
@patch('gcalcli.main.is_authentication_setup', return_value=False)
def test_main_when_running_configure(
        mock_is_setup, mock_load, mock_build, runner):
    result = runner.invoke(main, ['ls'])
    assert 'Looks like the app is not configured' in result.output
    assert result.exit_code == 1
    assert not mock_load.called
    assert not mock_build.called


@patch('gcalcli.main.setup_authentication')
@patch('gcalcli.main.is_authentication_setup')
def test_configure_when_success(mock_is_setup, mock_setup, runner):
    result = runner.invoke(configure)
    assert 'All done' in result.output
    assert result.exit_code == 0


@patch('gcalcli.main.setup_authentication')
@patch('gcalcli.main.is_authentication_setup', return_value=False)
def test_configure_when_fail(mock_is_setup, mock_setup, runner):
    result = runner.invoke(configure)
    assert 'Something went wrong' in result.output
    assert result.exit_code == 0


@patch('gcalcli.main.get_events')
def test_events_ls(mock_get_events, runner, event_json, ascii_table):
    mock_get_events.return_value = [event_json]
    result = runner.invoke(
        ls, ['--start', '01-11-2018', '--end', '30-11-2018']
    )

    assert result.output == ascii_table + '\n'
    assert result.exit_code == 0


@patch('gcalcli.main.get_events')
def test_events_ls_empty_table(
        mock_get_events, runner, event_json, ascii_table_headers_only):
    mock_get_events.return_value = []
    result = runner.invoke(
        ls, ['--start', '01-11-2018', '--end', '30-11-2018']
    )

    assert result.output == ascii_table_headers_only + '\n'
    assert result.exit_code == 0
