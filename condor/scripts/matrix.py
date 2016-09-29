"""
Implements the condor matrix commands to create term document matrices from
bibsets.
"""

import click


@click.group()
def matrix():
    """
    Term document matrix related commands.
    """
    pass


@matrix.command()
def create():
    """
    Create a new term document matrix.
    """
    pass


@matrix.command()
def list():
    """
    List all the available term document matrices.
    """
    pass


@matrix.command()
def delete():
    """
    Delete a given matrix and associated search engines.
    """
    pass
