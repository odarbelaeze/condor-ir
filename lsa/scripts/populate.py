'''
Implements the populate script.
'''

import glob
import sys

import click

from pymongo.errors import DuplicateKeyError

from lsa.record import BibtexRecordIterator
from lsa.record import FroacRecordIterator
from lsa.record import IsiRecordIterator

from .dbutil import collection
from .dbutil import collection_name


def recordset_class(name):
    '''
    Builds a record class out  of the `name` of the extension file.
    '''
    if name == 'isi':
        return IsiRecordIterator
    elif name == 'xml':
        return FroacRecordIterator
    elif name == 'froac':
        return FroacRecordIterator
    elif name == 'bib':
        return BibtexRecordIterator
    raise NotImplementedError('{} parser is not implemented yet'.format(name))


@click.command()
@click.argument('pattern')
@click.option('--xml', 'kind', flag_value='xml', default=True,
              help='Use the xml parser (default)')
@click.option('--froac', 'kind', flag_value='froac', default=True,
              help='Use the xml froac parser (default)')
@click.option('--isi', 'kind', flag_value='isi',
              help='Use the isi plain text parser (default xml)')
@click.option('--bib', 'kind', flag_value='bib',
              help='Use the bibtex parser (default xml)')
@click.option('--wipedb/--no-wipedb', default=True,
              help='Wipe existing database.')
@click.option('--dbname', default='program',
              help='Name of the mongo database to use to store the records')
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

    with collection('records', dbname=dbname, delete=wipedb) as records:
        for filename in glob.glob(pattern, recursive=True):
            if verbose:
                click.echo('I\'m processing file {}...'.format(filename))
            rs = rs_class(filename)
            for record in rs:
                try:
                    records.insert_one(record)
                except DuplicateKeyError:
                    continue

        click.echo('And... I\'m done')
        click.echo('The database contains {} records'.format(
            records.count()))
