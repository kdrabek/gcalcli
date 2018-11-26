import click

from googleapiclient.discovery import build

from gcalcli.authorization import (
    is_authentication_setup, load_credentials, setup_authentication)
from gcalcli.events import specs
from gcalcli.events.helpers import (
    to_table, validate_date, stringify, stringify2)
from gcalcli.events.api import get_events, create_event


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
@click.option('--start', '-s', required=True, type=str)
@click.option('--end', '-e', required=False, type=str, default=None)
@click.option('--filter', '-f', 'filter_', required=False, default=None)
@click.option('--show-deleted/--no-show-deleted', default=True)
def ls(calendar, start, end, filter_, show_deleted):
    flags = {
        'timeMin': stringify2(validate_date(start)),
        'timeMax': stringify2(validate_date(end)) if end else None,
        'filter': filter_,
        'showDeleted': show_deleted,
    }

    events = get_events(calendar, flags)
    parsed = specs.parse_events_list(events)
    click.echo(to_table(parsed))


@click.command()
@click.pass_obj
@click.option('--start', '-s', required=True, type=str)
@click.option('--end', '-e', required=True, type=str)
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
    flags = {
        'start': stringify(validate_date(start), add_timezone=True),
        'end': stringify(validate_date(end), add_timezone=True),
        'summary': title,
        'attendees': attendees,
        'status': status,
        'sendUpdates': send_updates
    }
    parsed = specs.serialize_create_event(flags)
    event = create_event(calendar, parsed)
    if event:
        click.echo(f'event added: {event}')
    else:
        click.echo('something went wrong')


main.add_command(ls)
main.add_command(add)
main.add_command(configure)


if __name__ == "__main__":
    main()
