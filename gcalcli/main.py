import click
from googleapiclient.discovery import build

from gcalcli.authorization import (
    is_authentication_setup, load_credentials, setup_authentication
)
from gcalcli.events import formatters
from gcalcli.events.api import create_event, get_events
from gcalcli.events.helpers import (
    convert_date, to_table, validate_date
)


@click.group()
@click.pass_context
def main(ctx):
    if is_authentication_setup():
        credentials = load_credentials()
        calendar = build('calendar', 'v3', credentials=credentials)
        ctx.obj = calendar

    if not is_authentication_setup() and ctx.invoked_subcommand != 'configure':
        click.echo(
            'Looks like the app is not configured.'
            'Please run "gcalcli configure"'
        )
        ctx.exit(code=1)


@click.command()
def configure():
    click.echo('Starting configuration...')
    setup_authentication()
    if is_authentication_setup():
        click.echo('All done. You\'re good to go')
    else:
        click.echo('Something went wrong. Try again please')


@click.command()
@click.pass_obj
@click.option('--start', '-s', required=True, type=str, callback=validate_date)
@click.option('--end', '-e', required=False, type=str, callback=validate_date, default=None)
@click.option('--filter', '-f', 'filter_', required=False, default=None)
@click.option('--show-deleted/--no-show-deleted', default=True)
def ls(calendar, start, end, filter_, show_deleted):
    flags = formatters.format_list_events_request({
        'start': start,
        'end': end,
        'filter': filter_,
        'show_deleted': show_deleted,
    })

    events = get_events(calendar, flags)
    formatted = formatters.format_events_list_response(events)
    click.echo(to_table(formatted))


@click.command()
@click.pass_obj
@click.option('--start', '-s', required=True, type=str, callback=validate_date)
@click.option('--end', '-e', required=True, type=str, callback=validate_date)
@click.option('--title', '-t', required=True)
@click.option('--attendees', '-a', required=False, multiple=True)
@click.option(
    '--status',
    type=click.Choice(['confirmed', 'tentative', 'cancelled']),
    default='confirmed'
)
@click.option(
    '--send-updates',
    type=click.Choice(['all', 'none']),
    default='none'
)
def add(calendar, start, end, title, attendees, status, send_updates):
    formatted = formatters.format_create_event_request({
        'start': start,
        'end': end,
        'summary': title,
        'attendees': attendees,
        'status': status,
        'send_updates': send_updates
    })

    event = create_event(calendar, formatted)
    if event:
        eid = event['id']
        click.echo(f'event added: {eid}')
    else:
        click.echo('something went wrong')


main.add_command(ls)
main.add_command(add)
main.add_command(configure)
