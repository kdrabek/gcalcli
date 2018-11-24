import click

from glom import glom
from googleapiclient.discovery import build

from gcalcli.authorization import (
    is_authentication_setup, load_credentials, setup_authentication)
from gcalcli.events import specs
from gcalcli.events.helpers import to_table, validate_date
from gcalcli.events.api import get_events


@click.group()
@click.pass_context
def main(ctx):
    if is_authentication_setup():
        credentials = load_credentials()
        calendar = build('calendar', 'v3', credentials=credentials)
        ctx.obj = calendar

    if not is_authentication_setup() and ctx.invoked_subcommand != 'configure':
        click.echo('Looks like the app is not configured. Please run $ gcalcli configure')
        ctx.exit(code=1)

    ctx.exit(code=0)


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
@click.option('--end', '-e', required=False, type=str, default=None, callback=validate_date)
@click.option('--filter', '-f', 'filter_', required=False, default=None)
@click.option('--show-deleted/--no-show-deleted', default=True)
def ls(calendar, start, end, filter_, show_deleted):
    flags = {
        'timeMin': start,
        'timeMax': end,
        'filter': filter_,
        'showDeleted': show_deleted,
    }
    events = get_events(calendar, flags)
    parsed = glom(events, [specs.event])
    click.echo(to_table(parsed))



@click.command()
@click.pass_obj
def add(calendar):
    click.echo('$ gcalcli add')


main.add_command(ls)
main.add_command(add)
main.add_command(configure)


if __name__ == "__main__":
    main()
