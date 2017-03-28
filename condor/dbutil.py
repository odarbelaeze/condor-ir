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
    exc,
)
from sqlalchemy.exc import OperationalError

from condor.config import DEFAULT_DB_PATH


def engine():
    """
    Creates an engine to handle our database.
    """
    # Use a sqlite database by default.
    default_url = 'sqlite:///' + os.path.join(DEFAULT_DB_PATH, 'condor.db')
    url = os.environ.get('CONDOR_DB_URL', default_url)
    return create_engine(url)


def session():
    """
    Creates a session maker instance attached to our default engine.
    """
    return scoped_session(sessionmaker(bind=engine()))


def requires_db(func):
    """
    Injects a database session into a function as first argument.

    Checks if the db is available and we can create a session otherwise errors
    out, if the database is available, it tries to run the underlying function
    and commit any changes to the database, if something fails, it rolls back
    any uncommitted changes.

    .. note::
        for best results use `db.flush()` instead of `db.commit()` in functions
        that require a database connection.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check for the database
        try:
            db = session()
            try:
                # Execute the function, commit and return
                result = func(db, *args, **kwargs)
                db.commit()
                return result
            except Exception as e:
                # Rollback the database if anything bad happens
                click.echo(click.style(
                    'Rolling back the database.',
                    fg='yellow'
                ))
                db.rollback()
                raise e
        except OperationalError as e:
            click.echo(click.style(
                'There was an error connecting to the database.',
                fg='red'
            ))
            raise e
            sys.exit(1)
    return wrapper


def find_one(db, model, eid):
    """
    Finds exactly one of the given models in the db by eid.

    It's useful when trying to delete or show an item, if we don't know such
    item we might as well exit the program.

    :param db: db connection instance
    :param model: model to look for, should have an eid field
    :param eid: part of the eid to look for
    :return: the instance of the model found
    """
    try:
        return db.query(model).filter(
            model.eid.like(eid + '%')
        ).one()
    except exc.NoResultFound:
        click.secho('Could not find a result matching {}'.format(eid), fg='red')
        raise click.Abort()
    except exc.MultipleResultsFound:
        click.secho('Found many results matching {}'.format(eid), fg='red')
        raise click.Abort()


def one_or_latest(db, model, eid):
    """
    Finds an instance of the given model if the eid is provided otherwise returns the
    latest created in the database. If there's no instance in the database, returns
    None.

    :param db: db connection instance
    :param model: model to look for, should have an eid field
    :param eid: part of the eid to look for
    :return: the instance of the model found
    """
    if eid is None:
        return db.query(model).order_by(
            model.created.desc()
        ).first()
    return find_one(db, model, eid)
