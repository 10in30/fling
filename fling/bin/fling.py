#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Fling CLI commands
"""
import json
from pprint import pprint
import click
from cookiecutter.main import cookiecutter
from ..fling_client.client import Client
from ..fling_client.api.names import generate_names_namer_get


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
    fling_client = Client('https://fling-virid.vercel.app')
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


def main():
    fling(obj={})


if __name__ == "__main__":
    main()
