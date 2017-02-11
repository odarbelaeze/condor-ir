'''
Implements the populate script.
'''

import glob
import itertools
import sys

import click
import sqlalchemy
import tabulate

from condor.record import BibtexRecordIterator
from condor.record import FroacRecordIterator
from condor.record import IsiRecordIterator

from condor.dbutil import session, requires_db

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
            keywords = record.get('keywords', [])
            record['keywords'] = '; '.join(keywords)
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


@click.group()
def bibset():
    """
    Bibliography set related commands.
    """
    pass


@bibset.command()
@click.option('--count', default=10, help='Number of bibsets.')
@requires_db
def list(count):
    """
    List all the bibliography sets.
    """
    bibliography_sets = session().query(BibliographySet).order_by(
        BibliographySet.created.desc()
    ).limit(count)

    click.echo(
        tabulate.tabulate(
            [
                [
                    bibset.eid[:8],
                    bibset.description,
                    bibset.modified.strftime('%b %d, %Y, %I:%M%p'),
                    len(bibset.bibliographies)
                ]
                for bibset in bibliography_sets
            ],
            headers=[
                'Identifier', 'Description', 'Updated at', 'Docs count',
            ],
            tablefmt='rst',
        )
    )
    total = session().query(BibliographySet).count()
    if count >= total:
        click.echo('Showing all the bibsets.')
    else:
        click.echo(
            'Shwoing {count} out of {total} bibliography sets.'
            .format(count=count, total=total)
        )


@bibset.command()
@click.argument('target')
@requires_db
def delete(target):
    """
    Delete the target bibliography set.
    """
    db = session()
    try:
        bibliography_set = db.query(BibliographySet).filter(
            BibliographySet.eid.like(target + '%')
        ).one()
    except sqlalchemy.orm.exc.NoResultFound:
        click.echo('Could not find a result matching {}'.format(target))
        return
    except sqlalchemy.orm.exc.MultipleResultsFound:
        click.echo('Found many results matching {}'.format(target))
        return

    click.echo(
        'I will delete the bibliography set {}.'
        .format(bibliography_set.eid)
    )
    click.echo('And also {} bibliographies.'
               .format(len(bibliography_set.bibliographies)))
    click.echo('And also {} term document matrices.'
               .format(len(bibliography_set.term_document_matrices)))
    click.echo('And also {} search engines.'
               .format(len([
                   rm
                   for tdm in bibliography_set.term_document_matrices
                   for rm in tdm.ranking_matrices
               ])))
    click.confirm('Do you want me to delete all this information?', abort=True)
    db.delete(bibliography_set)
    db.commit()


@bibset.command()
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
@requires_db
def create(pattern, kind, verbose, chunk_size):
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


if __name__ == "__main__":
    bibset()
