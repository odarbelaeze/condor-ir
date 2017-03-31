"""
Implements the condor matrix commands to create term document matrices from
bibsets.
"""

import sys

import click
import sqlalchemy
import tabulate

from condor.dbutil import requires_db, one_or_latest
from condor.models import BibliographySet, TermDocumentMatrix


@click.group()
def matrix():
    """
    Term document matrix related commands.
    """
    pass


@matrix.command()
@click.option('--target', default=None, type=str,
              help='Bibliography set to work with')
@click.option('--regularise/--no-regularise', default=True,
              help='Apply TF-IDF regularisation to the matrix')
@click.option('--field', '-f', 'fields', multiple=True, type=str, default=None,
              help='Use these fields on matrix creation.')
@click.option('--verbose/--quiet', default=False,
              help='Be more verbose')
@requires_db
def create(db, target, regularise, fields, verbose):
    """
    Create a new term document matrix.
    """

    bibliography_set = one_or_latest(db, BibliographySet, target)
    if bibliography_set is None:
        click.echo('Please create a bibset first')
        sys.exit(1)

    if verbose:
        click.echo('I will generate a matrix for the {} bibset...'.format(
            bibliography_set.eid))

    td_matrix = TermDocumentMatrix.from_bibliography_set(
        bibliography_set, regularise=regularise, fields=fields
    )

    click.secho('Done!', fg='green')

    db.add(td_matrix)


@matrix.command()
@click.option('--count', default=10, help='Number of bibsets.')
@requires_db
def list(db, count):
    """
    List all the available term document matrices.
    """
    term_doc_matrices = db.query(TermDocumentMatrix).order_by(
        TermDocumentMatrix.created.desc()
    ).limit(count)

    click.echo(
        tabulate.tabulate(
            [
                [
                    td.eid[:8],
                    td.bibliography_set.eid[:8],
                    td.created.strftime('%b %d, %Y, %I:%M%p'),
                    td.modified.strftime('%b %d, %Y, %I:%M%p'),
                ]
                for td in term_doc_matrices
            ],
            headers=[
                'Identifier', 'Bibliography Set', 'Created at', 'Updated at'
            ],
            tablefmt='rst',
        )
    )
    total = db.query(TermDocumentMatrix).count()
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
def delete(db, target):
    """
    Delete a given matrix and associated search engines.
    """
    try:
        term_document_matrix = db.query(TermDocumentMatrix).filter(
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
    db.delete(term_document_matrix)
