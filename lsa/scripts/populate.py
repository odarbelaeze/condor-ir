import contextlib
import glob
import sys

import click
import pymongo

from pymongo.errors import DuplicateKeyError

from lsa.record import FroacRecordSet
from lsa.record import IsiRecordSet


# That global mongo client
MONGO_CLIENT = pymongo.MongoClient('localhost', 27017)


def collection_name(name):
    '''
    Prepends 'lsa-' to the given name.
    '''
    return 'lsa-' + name


def recordset_class(name):
    if name == 'isi':
        return IsiRecordSet
    elif name == 'xml':
        return FroacRecordSet
    raise NotImplementedError('{} parser is not implemented yet'.format(name))


@contextlib.contextmanager
def collection(dbname='records', delete=True):
    '''
    Returns a collection from the mongo database
    '''
    database = MONGO_CLIENT['lsa-' + dbname]
    records = database['records']
    if delete:
        records.delete_many({})
    records.create_index([('uuid', pymongo.ASCENDING)], unique=True)
    yield records


@click.command()
@click.argument('pattern')
@click.option('--xml', 'kind', flag_value='xml', default=True,
              help='Use the xml parser (default)')
@click.option('--isi', 'kind', flag_value='isi',
              help='Use the isi plain text parser (default xml)')
@click.option('--wipedb/--no-wipedb', default=True,
              help='Wipe existing database.')
@click.option('--dbname', default='program',
              help='Name of the mongo collection to use to store the records')
@click.option('--verbose/--quiet', default=False,
              help='Be more verbose')
def lsapopulate(pattern, kind, wipedb, dbname, verbose):
    '''
    Populates a mongo database collection with all the records it can find
    in the files matching the provided `PATTERN`, the parser will be determined
    usint the kind flags.

    'lsa-' will be prepended to the database name provided thorugh the
    `--dbname` flag.
    '''

    click.echo('I\'m looking for {} records in files matching {}'.format(
        kind, pattern))

    if wipedb:
        click.echo('I will delete all previous records in the records \
collection of the {} database...'.format(
                collection_name(dbname))
        )

    try:
        rs_class = recordset_class(kind)
    except NotImplementedError as e:
        click.echo('Sadly, ' + e.message)
        sys.exit(1)

    with collection(dbname=dbname, delete=wipedb) as records:
        for filename in glob.glob(pattern):
            if verbose:
                click.echo('I\'m processing file {}...'.format(filename))
            rs = rs_class(filename)
            for record in rs.metadata():
                try:
                    records.insert_one(record)
                except DuplicateKeyError:
                    continue

        click.echo('And... I\'m done')
        click.echo('The database contains {} records'.format(
            records.count()))
