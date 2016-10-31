"""This module includes utility scripts.

Such as creating and wiping the db and others in the future.
"""

import click

from condor.models.base import DeclarativeBase
from condor.dbutil import requires_db, engine


@click.group()
def utils():
    """Utilities for managing the condor program.
    """


@utils.command()
@requires_db
def preparedb():
    """Wipes out and creates all the tables on the db.

    This is meant to be used with care, all data will be lost after running
    this command.
    """
    click.echo(
        click.style(
            'This command will delete all your tables if they exists careful '
            'with it', fg='yellow'
        )
    )
    click.confirm('Do you want me to reset the database schema?', abort=True)
    _engine = engine()
    DeclarativeBase.metadata.drop_all(_engine)
    DeclarativeBase.metadata.create_all(_engine)
    click.echo(
        click.style(
            'Successfully created the database schema.', fg='green'
        )
    )
