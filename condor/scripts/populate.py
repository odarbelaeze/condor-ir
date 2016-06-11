'''
Implements the populate script.
'''

import glob
import itertools
import sys

import click

from condor.record import BibtexRecordIterator
from condor.record import FroacRecordIterator
from condor.record import IsiRecordIterator

from condor.dbutil import session

from condor.models import Bibliography
from condor.models import BibliographySet


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


def describe_bibset(kind, pattern):
    desc = 'Bibliography set created from {kind} files ussing {pattern}'
    return BibliographySet(
        description=desc.format(kind=kind, pattern=pattern)
    )


def find_records(pattern, klass, verbose=False):
    for filename in glob.glob(pattern, recursive=True):
        if verbose:
            click.echo('I\'m processing file {}...'.format(filename))
        rs = klass(filename)
        for record in rs:
            yield record


def chunks(sequence, n):
    seq_it = iter(sequence)
    while True:
        chunk = itertools.islice(seq_it, n)
        try:
            first_el = next(chunk)
        except StopIteration:
            return
        yield itertools.chain((first_el, ), chunk)


def existing_bibliographies(db, bibset, hashes):
    query = db.query(Bibliography).join(BibliographySet)
    query = query.filter(BibliographySet.eid == bibset.eid)
    query = query.filter(Bibliography.hash.in_(hashes))
    return query.all()


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
@click.option('--verbose/--quiet', default=False,
              help='Be more verbose')
@click.option('--chunk-size', default=1000,
              help='Insert into db in chunks')
def condorpopulate(pattern, kind, verbose, chunk_size):
    '''
    Populates a mongo database collection with all the records it can find
    in the files matching the provided `PATTERN`, the parser will be determined
    usint the kind flags.
    '''

    click.echo('I\'m looking for {} records in files matching {}'.format(
        kind, pattern))

    try:
        rs_class = recordset_class(kind)
    except NotImplementedError as e:
        click.echo('Sadly, ' + e.message)
        sys.exit(1)

    db = session()
    bibset = describe_bibset(kind, pattern)
    db.add(bibset)
    db.commit()

    click.echo('I\'m writting to {bibset.eid}'.format(bibset=bibset))

    records = find_records(pattern, rs_class, verbose=verbose)
    for chunk in chunks(records, chunk_size):
        record_hash = {
            record['hash']: record
            for record in chunk
        }

        # Filter out existing bibliography records
        for bib in existing_bibliographies(db, bibset, record_hash.keys()):
            record_hash.pop(bib.hash)

        db.bulk_insert_mappings(
            Bibliography,
            [
                dict(bibliography_set_eid=bibset.eid, **record)
                for record in record_hash.values()
            ]
        )
        db.commit()

    click.echo('And... I\'m done')
    click.echo('The database contains {} records'.format(
        db.query(Bibliography).join(BibliographySet).
        filter(BibliographySet.eid == bibset.eid).
        count()
    ))
