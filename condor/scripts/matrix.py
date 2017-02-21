"""
Implements the condor matrix commands to create term document matrices from
bibsets.
"""

import click
import numpy
import os
import sqlalchemy
import sys
import tabulate

from condor.dbutil import requires_db
from condor.models import BibliographySet, TermDocumentMatrix
from condor.builders.matrix import build_matrix
from condor.config import MATRIX_PATH, TERM_LIST_PATH


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
@click.option('--verbose/--quiet', default=False,
              help='Be more verbose')
@requires_db
def create(db, target, regularise, verbose):
    """
    Create a new term document matrix.
    """
    if target is None:
        bibset = BibliographySet.latest(db)
    else:
        bibset = BibliographySet.find_by_eid(db, target)

    if bibset is None:
        click.echo('Please create a bibset first')
        sys.exit(1)

    click.echo('I will generate a matrix for the {} bibset...'.format(
        bibset.eid))

    words, frequency, options, matrix_hash = build_matrix(bibset, regularise)
    nwords, nrecs = frequency.shape

    matrix_filename = os.path.join(MATRIX_PATH, '{}.npy'.format(matrix_hash))
    click.echo(
        'Storing the term document matrix at {}'
        .format(matrix_filename)
    )
    numpy.save(matrix_filename, frequency)

    term_list_filename = os.path.join(
        TERM_LIST_PATH, '{}.txt'.format(matrix_hash)
    )
    click.echo(
        'Storing the term list at {}'.format(TERM_LIST_PATH)
    )
    with open(term_list_filename, 'w') as file:
        file.write('\n'.join(words))

    td_matrix = TermDocumentMatrix(
        bibliography_options='',
        processing_options=options,
        term_list_path=term_list_filename,
        tdidf_matrix_path=matrix_filename,
    )
    td_matrix.bibliography_set = bibset
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
