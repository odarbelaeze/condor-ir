'''
Utils to work with a mongo database, it contains a global connection to the
database so that a new one is not created with every request which is a huge
overhead. Furthermore it has a tool to use a pymongo collection as a context
manager.
'''

import click
import functools
import sys
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from sqlalchemy.exc import OperationalError

from condor.config import DEFAULT_DB_PATH


def engine():
    """Creates an engine to handle our database.
    """
    # Use a sqlite database by default.
    default_url = 'sqlite:///' + os.path.join(DEFAULT_DB_PATH, 'condor.db')
    url = os.environ.get('CONDOR_DB_URL', default_url)
    return create_engine(url)


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
            return func(*args, **kwargs)
        except OperationalError as e:
            click.echo(
                click.style('There was an error connectig to the database.',
                            fg='red')
            )
            raise e
            sys.exit(1)
    return wrapper
