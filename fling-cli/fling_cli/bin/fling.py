#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Fling CLI commands
"""
# from pprint import pprint
import rich_click as click
# import rich
# from rich.progress import Progress
from rich import print
from rich.tree import Tree
from cookiecutter.main import cookiecutter
from fling_client.client import Client
from fling_client.api.names import generate_names_namer_get
from rich.table import Table
from fling_core import settings


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
    pass


@fling.command(
    help="Search for a name that's available everywhere"
)
@click.pass_context
@click.argument("phrase")
def search(ctx, phrase):
    # fling_id = ctx.obj["fling_id"]
    fling_client = Client(settings.fling.api_server, timeout=60)
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
    try:
        with open('fling.yaml', 'r') as fling_file:
            print("[bold green]Public side project status info[/bold green]")
            print(fling_file.read())
    except FileNotFoundError:
        print("Doesn't look like this side project is under fling management.")
        return
    print("[bold green]Private side project status info...[/bold green]")
    print("[grey]...fetching from fling servers...[/grey]")
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
    print("[red]Not yet implemented.[/red]")


def main():
    fling(obj={})


if __name__ == "__main__":
    main()
