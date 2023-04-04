#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Fling CLI commands
"""
import json
from pprint import pprint
import click
from ..fast_api_client.client import Client
from ..fast_api_client.api.root import read_root_get


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
    names = read_root_get.sync(client=fling_client, phrase=word).to_dict()
    pprint(names)


@fling.command(
    help="Search for a name that's available everywhere"
)
@click.pass_context
@click.argument("word")
def init(ctx, word):
    pass


def main():
    fling(obj={})


if __name__ == "__main__":
    main()
