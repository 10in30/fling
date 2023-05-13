#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Fling CLI commands
"""
import hashlib
from pathlib import Path
import pathlib
from fling_cli.auth import gh_authenticate
from fling_cli import get_fling_client
import rich_click as click
from click.exceptions import UsageError
from rich import print, print_json
from rich.tree import Tree
from cookiecutter.main import cookiecutter
from fling_client.api.names import generate_names_namer_get
from fling_client.api.data import (
    add_data_fling_id_add_post,
    read_data_fling_id_get,
    get_repo_list_repolist_get,
    add_to_index_index_put,
    read_index_index_get,
)
from rich.table import Table
import gitinfo
from git import Repo
from giturlparse import parse



click.rich_click.USE_RICH_MARKUP = True
click.rich_click.COMMAND_GROUPS = {
    "fling": [
        {
            "name": "Commands for starting new projects",
            "commands": ["auth", "search", "init", "acknowledge"],
        },
        {
            "name": "Commands for managing fling data",
            "commands": ["add", "status", "pull"],
        },
        {
            "name": "Advanced commands",
            "commands": ["repolist", "breakup"],
        },
    ]
}


@click.group()
@click.pass_context
@click.option("-v", "--verbose", is_flag=True, default=False)
def fling(ctx, verbose):
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    logo_path = pathlib.Path(__file__).parent.parent / "logo-hc.txt"
    with open(logo_path, "r") as logo:
        print(f"[green]{logo.read()}[/green]", end="")
    print()


@fling.command(help="Authenticate with GitHub")
@click.pass_context
def auth(ctx):
    gh_authenticate()


@fling.command(help="Search for a name that's available everywhere")
@click.pass_context
@click.argument("project_phrase")
def search(ctx, project_phrase):
    # fling_id = ctx.obj["fling_id"]
    names = generate_names_namer_get.sync(
        client=get_fling_client(), phrase=project_phrase
    )
    if not names:
        raise UsageError("No names found")
    ctx.obj["names"] = names.to_dict()
    print_json(data=ctx.obj["names"])


@fling.command(help="Create a new side project")
@click.pass_context
@click.argument("project_name")
def init(ctx, project_name):
    cookiecutter(
        "https://github.com/herdwise/cookiecutter-fling.git",
        extra_context={"project_name": project_name},
    )


@fling.command(
    help="Acknowledge an existing side project and import it into the Fling service"
)
@click.pass_context
@click.option("-fl", "--fling_id", required=False, type=str)
def acknowledge(ctx, fling_id=None):
    if not fling_id:
        fling_id = fling_id_from_cwd()
    add_fling_to_index(fling_id)


def fling_id_from_cwd():
    current_repo = gitinfo.get_git_info()
    if not current_repo:
        raise UsageError(
            "You must run acknowledge from inside a git working directory."
        )
    git_cwd = Path(current_repo["gitdir"]).parent
    repo = Repo(git_cwd)
    p = parse(repo.remotes.origin.url)
    return f"{p.host}/{p.owner}/{p.repo}"


def add_fling_to_index(fling_id):
    fling_client = get_fling_client(require_auth=True)
    try:
        add_to_index_index_put.sync(client=fling_client, fling_id=fling_id)
        print(f"[green]Project `{fling_id}` has been added to fling[/green]")
    except:
        raise UsageError("You don't have the right permissions to do that.")


@fling.command(help="List all repos on github")
@click.pass_context
@click.option(
    "-ack",
    "--acknowledge",
    is_flag=True,
    show_default=True,
    default=False,
    help="Add all repos to fling.",
)
def list_repos(ctx, acknowledge):
    repos = get_repo_list_repolist_get.sync(client=get_fling_client(require_auth=True))
    [print(f"{x['full_name']}: private? {x['private']}") for x in repos]
    if acknowledge:
        for x in repos:
            fling_id = f"github.com/{x['full_name']}"
            add_fling_to_index(fling_id)


@fling.command(help="List all flings")
@click.pass_context
def list_flings(ctx):
    projects = read_index_index_get.sync(
        client=get_fling_client(require_auth=True)
    ).to_dict()
    [print(f"{x}") for x in projects.keys()]


@fling.command(help="Cancel all fling-connected services and shut it down!")
@click.pass_context
def breakup(ctx):
    print("[red]Not yet implemented.[/red]")


@fling.command(help="Check on the overall status of this project")
@click.pass_context
@click.option("-fl", "--fling_id", required=False, type=str)
def status(ctx, fling_id=None):
    if not fling_id:
        fling_id = fling_id_from_cwd()
    hashed_fling_id = hashlib.md5(fling_id.encode("utf-8")).hexdigest()
    current_data = read_data_fling_id_get.sync(
        client=get_fling_client(require_auth=True), fling_id=hashed_fling_id
    ).to_dict()

    tree = Tree(f"[bold green]{fling_id}[/bold green]")
    print("[dim]...fetching from fling servers...[/dim]")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Key", style="dim")
    table.add_column("Value")
    # table.add_column("Production Budget", justify="right")
    # table.add_column("Box Office", justify="right")
    [table.add_row(key, current_data[key]) for key in current_data]
    tree.add(table)

    baz_tree = tree.add("Local Fling Config")
    baz_tree.add("[red]Red")
    print(tree)


@fling.command(
    help="Fetch current state from configured plugins and update your fling DB"
)
@click.pass_context
def pull(ctx):
    print("[red]Not yet implemented.[/red]")


@fling.command(help="Add some arbitrary data to fling DB")
@click.pass_context
@click.argument("key")
@click.argument("val")
@click.option("-fl", "--fling_id", required=False, type=str)
def add(ctx, key, val, fling_id=None):
    if not fling_id:
        fling_id = fling_id_from_cwd()
    hashed_fling_id = hashlib.md5(fling_id.encode("utf-8")).hexdigest()
    added_data = add_data_fling_id_add_post.sync(
        client=get_fling_client(require_auth=True),
        fling_id=hashed_fling_id,
        key=key,
        val=val,
    )
    click.echo(added_data)


@fling.command(help="Current version")
def version():
    from .. import __version__
    print(f"Current version: {__version__}")


def main():
    return fling(obj={})


if __name__ == "__main__":
    main()
