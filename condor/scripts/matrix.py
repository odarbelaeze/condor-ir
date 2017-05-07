"""
Implements the condor matrix commands to create term document matrices from
bibsets.
"""

import sys

import click
import sqlalchemy
import tabulate

from condor.dbutil import requires_db, one_or_latest
from condor.models import Bibliography, TermDocumentMatrix


@click.group()
def matrix():
    """
    Term document matrix related commands.
    """
    pass


@matrix.command()
@click.option('--target', default=None, type=str,
              help='Document set to work with')
@click.option('--regularise/--no-regularise', default=True,
              help='Apply TF-IDF regularisation to the matrix')
@click.option('--field', '-f', 'fields', multiple=True, type=str, default=None,
              help='Use these fields on matrix creation.')
@click.option('--verbose/--quiet', default=False,
              help='Be more verbose')
@requires_db
def create(database, target, regularise, fields, verbose):
    """
    Create a new term document matrix.
    """

    bibliography = one_or_latest(database, Bibliography, target)
    if bibliography is None:
        click.echo('Please create a bibliography first')
        sys.exit(1)

    if verbose:
        click.echo('I will generate a matrix for the {} bibliography...'.format(
            bibliography.eid))

    td_matrix = TermDocumentMatrix.from_bibliography_set(
        bibliography, regularise=regularise, fields=fields
    )

    click.secho('Done!', fg='green')

    database.add(td_matrix)


@matrix.command('list')
@click.option('--count', default=10, help='Number of bibsets.')
@requires_db
def list_matrices(database, count):
    """
    List all the available term document matrices.
    """
    term_doc_matrices = TermDocumentMatrix.list(database, count)

    click.echo(
        tabulate.tabulate(
            [
                [
                    td.eid[:8],
                    td.bibliography.eid[:8],
                    td.created.strftime('%b %d, %Y, %I:%M%p'),
                    td.modified.strftime('%b %d, %Y, %I:%M%p'),
                ]
                for td in term_doc_matrices
            ],
            headers=[
                'Identifier', 'Document Set', 'Created at', 'Updated at'
            ],
            tablefmt='rst',
        )
    )
    total = TermDocumentMatrix.count(database)
    if count >= total:
        click.echo('Showing all the term document matrices.')
    else:
        click.echo(
            'Shwoing {count} out of {total} term document matrices.'
            .format(count=count, total=total)
        )


@matrix.command()
@click.argument('target')
@requires_db
def delete(database, target):
    """
    Delete a given matrix and associated search engines.
    """
    try:
        term_document_matrix = database.query(TermDocumentMatrix).filter(
            TermDocumentMatrix.eid.like(target + '%')
        ).one()
    except sqlalchemy.orm.exc.NoResultFound:
        click.echo('Could not find a result matching {}'.format(target))
        return
    except sqlalchemy.orm.exc.MultipleResultsFound:
        click.echo('Found many results matching {}'.format(target))
        return

    click.echo(
        'I will delete the term document matrix {}.'
        .format(term_document_matrix.eid)
    )
    click.echo('And also {} search engines.'
               .format(len(term_document_matrix.ranking_matrices)))
    click.confirm('Do you want me to delete all this information?', abort=True)
    database.delete(term_document_matrix)
