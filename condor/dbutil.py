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


def session():
    return scoped_session(sessionmaker(bind=create_engine(
        'postgresql://condor-ir:condor-ir@localhost/condor-ir'
    )))


def requires_db(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check for the database
        try:
            session()
            return func(*args, **kwargs)
        except:
            click.echo(
                click.style('There was an error connectig to the database.',
                            fg='red')
            )
            sys.exit(1)
    return wrapper
