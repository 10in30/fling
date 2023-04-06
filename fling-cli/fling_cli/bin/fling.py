#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Fling CLI commands
"""
# from pprint import pprint
from fling_cli.auth import gh_authenticate
import keyring
import rich_click as click
# import rich
# from rich.progress import Progress
from rich import print
from rich.tree import Tree
from cookiecutter.main import cookiecutter
from fling_client.client import Client
from fling_client.api.names import generate_names_namer_get
from fling_client.api.data import add_data_fling_id_add_post, read_data_fling_id_get
from rich.table import Table
from fling_core import settings


fling_client = Client(settings.fling.api_server, timeout=60)

click.rich_click.USE_RICH_MARKUP = True
click.rich_click.COMMAND_GROUPS = {
    "fling.py": [
        {
            "name": "Commands for starting new projects",
            "commands": ["search", "init", 'acknowledge'],
        },
        {
            "name": "Commands for managing fling data",
            "commands": ["add", "status", "pull"],
        },
        {
            "name": "Advanced commands",
            "commands": ["breakup"],
        },
    ]
}


@click.group(chain=True)
@click.pass_context
def fling(ctx):
    ctx.ensure_object(dict)


@fling.command(
    help="Search for a name that's available everywhere"
)
@click.pass_context
@click.argument("phrase")
def search(ctx, phrase):
    # TODO: Auth decorator
    username = "joshuamckenty"
    token = keyring.get_password("fling-github-token", username)
    if not token:
        raise Exception("No token found, please run ```fling auth``` first.")
    # fling_id = ctx.obj["fling_id"]
    names = generate_names_namer_get.sync(client=fling_client, phrase=phrase)
    # async with generate_names_namer_get.asyncio_detailed(client=fling_client, phrase=word) as names:
    #     with Progress(
    #         "[progress.percentage]{task.percentage:>3.0f}%",
    #         rich.progress.BarColumn(bar_width=None),
    #         rich.progress.DownloadColumn(),
    #         rich.progress.TransferSpeedColumn(),
    #     ) as progress:
    #         download_task = progress.add_task("Download", total=100)
    #         progress.update(download_task, completed=names.num_bytes_downloaded)
    if not names:
        raise "No names found"
    ctx.obj["names"] = names.to_dict()
    click.echo(ctx.obj["names"])


@fling.command(
    help="Create a new side project"
)
@click.pass_context
@click.argument("word")
def init(ctx, word):
    cookiecutter('https://github.com/herdwise/cookiecutter-fling.git',
                 extra_context={"project_name": word})


@fling.command(
    help="Authenticate with GitHub"
)
@click.pass_context
def auth(ctx):
    gh_authenticate()



@fling.command(
    help="Acknowledge an existing side project and import it into the Fling service"
)
@click.pass_context
def acknowledge(ctx):
    print("[red]Not yet implemented.[/red]")


@fling.command(
    help="Cancel all fling-connected services and shut it down!"
)
@click.pass_context
def breakup(ctx):
    print("[red]Not yet implemented.[/red]")


@fling.command(
    help="Check on the overall status of this project"
)
@click.pass_context
def status(ctx):
    tree = Tree("Fling Status Tree")
    print("[bold green]Private side project status info...[/bold green]")
    print("[grey]...fetching from fling servers...[/grey]")
    if not settings.get("project_name"):
        raise "Doesn't look like a fling project here, or the init isn't completed."
    current_data = read_data_fling_id_get.sync(client=fling_client, fling_id=settings.project_name)
    click.echo(current_data)

    baz_tree = tree.add("baz")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Date", style="dim", width=12)
    table.add_column("Title")
    table.add_column("Production Budget", justify="right")
    table.add_column("Box Office", justify="right")
    table.add_row(
        "Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$275,000,000", "$375,126,118"
    )
    table.add_row(
        "May 25, 2018",
        "[red]Solo[/red]: A Star Wars Story",
        "$275,000,000",
        "$393,151,347",
    )
    table.add_row(
        "Dec 15, 2017",
        "Star Wars Ep. VIII: The Last Jedi",
        "$262,000,000",
        "[bold]$1,332,539,889[/bold]",
    )
    baz_tree.add("[red]Red").add("[green]Green").add(table)
    print(tree)


@fling.command(
    help="Fetch current state from configured plugins and update your fling DB"
)
@click.pass_context
def pull(ctx):
    print("[red]Not yet implemented.[/red]")


@fling.command(
    help="Add some arbitrary data to fling DB"
)
@click.pass_context
@click.argument("key")
@click.argument("val")
def add(ctx, key, val):
    if not settings.get("project_name"):
        raise "Doesn't look like a fling project here, or the init isn't completed."
    added_data = add_data_fling_id_add_post.sync(client=fling_client, fling_id=settings.project_name, key=key, val=val)
    click.echo(added_data)


def main():
    fling(obj={})


if __name__ == "__main__":
    main()
