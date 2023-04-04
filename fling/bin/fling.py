#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Fling CLI commands
"""
import click


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
    pass


def main():
    fling(obj={})


if __name__ == "__main__":
    main()
