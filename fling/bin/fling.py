#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Fling CLI commands
"""
from pprint import pprint
import rich_click as click
from rich import print
from rich.tree import Tree
from cookiecutter.main import cookiecutter
from ..fling_client.client import Client
from ..fling_client.api.names import generate_names_namer_get


click.rich_click.USE_RICH_MARKUP = True


@click.group()
@click.pass_context
def fling(context):
    pass


@fling.command(
    help="Search for a name that's available everywhere"
)
@click.pass_context
@click.argument("word")
def search(ctx, word):
    fling_client = Client('https://fling-virid.vercel.app', timeout=30)
    names = generate_names_namer_get.sync(
        client=fling_client, phrase=word)
    pprint(names and names.to_dict() or "No names found")


@fling.command(
    help="Search for a name that's available everywhere"
)
@click.pass_context
@click.argument("word")
def init(ctx, word):
    # JMC: Do the cookiecutter stuff here
    # Create project from the cookiecutter-pypackage.git repo template
    cookiecutter('https://github.com/herdwise/cookiecutter-fling.git')


@fling.command(
    help="Check on the overall status of this project"
)
@click.pass_context
def status(ctx):
    tree = Tree("Fling Status Tree")
    try:
        with open('fling.yaml', 'r') as fling_file:
            print("[bold green]Public side project status info...[/bold green]")
            print(fling_file.read())
    except FileNotFoundError:
        print("Doesn't look like this side project is under fling management yet.")
        return
    print("[bold green]Private side project status info...[/bold green]")
    print("[grey]...fetching from fling servers...[/grey]")
    baz_tree = tree.add("baz")
    baz_tree.add("[red]Red").add("[green]Green").add("[blue]Blue")
    print(tree)


def main():
    fling(obj={})


if __name__ == "__main__":
    main()
