"""
Functions to work with a contributed set of queries from the command line.
"""

import click


@click.group()
def contributor():
    """
    Manages contributor queries.
    """


@contributor.command()
def create():
    click.echo('And now...')