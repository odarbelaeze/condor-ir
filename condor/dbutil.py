'''
Utils to work with a mongo database, it contains a global connection to the
database so that a new one is not created with every request which is a huge
overhead. Furthermore it has a tool to use a pymongo collection as a context
manager.
'''

import click
import functools
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)


def engine():
    """Creates an engine to handle our database.
    """
    return create_engine(
        'postgresql://condor-ir:condor-ir@localhost/condor-ir'
    )


def session():
    """Creates a session maker instance attached to our default engine.
    """
    return scoped_session(sessionmaker(bind=engine()))


def requires_db(func):
    """Checks if the db is available and we can create a session.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check for the database
        try:
            session()
        # TODO: Be specific with this exception.
        except:
            click.echo(
                click.style('There was an error connectig to the database.',
                            fg='red')
            )
            sys.exit(1)
        return func(*args, **kwargs)
    return wrapper
