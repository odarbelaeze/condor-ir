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
from condor.models import (
    TermDocumentMatrix,
    RankingMatrix
)
from condor.builders.ranking import build_lsa_ranking
from condor.config import MODEL_PATH


@click.group()
def ranking():
    """
    Term document matrix related commands.
    """
    pass


@ranking.command()
@click.option('--target', default=None, type=str,
              help='Bibliography set to work with')
@click.option('--verbose/--quiet', default=False,
              help='Be more verbose')
@requires_db
def create(db, target, verbose):
    """
    Create a new term document matrix.
    """
    # TODO: Throw this into db_util.
    if target is None:
        td_matrix = TermDocumentMatrix.latest(db)
    else:
        td_matrix = TermDocumentMatrix.find_by_eid(db, target)
    if td_matrix is None:
        click.echo('Please create a bibset first')
        sys.exit(1)

    click.echo('I will generate a ranking for the {} term doc matrix.'.format(
        td_matrix.eid))

    ranking_result = build_lsa_ranking(td_matrix, covariance=0.8)

    if verbose:
        nwords, nrecs = ranking_result.ranking.shape
        click.echo('I\'ve removed noise from the freq mat...')
        click.echo('Number of records: {}'.format(nrecs))
        click.echo('Number of words: {}'.format(nwords))

    model_filename = os.path.join(
        MODEL_PATH,
        '{}.npy'.format(ranking_result.hash)
    )
    click.echo(
        'Storing the ranking matrix at {}'
        .format(model_filename)
    )
    numpy.save(model_filename, ranking_result.ranking)

    ranking_matrix = RankingMatrix(
        kind='lsa',
        build_options=ranking_result.options,
        ranking_matrix_path=model_filename,
    )
    ranking_matrix.term_document_matrix = td_matrix
    db.add(ranking_matrix)


@ranking.command()
@click.option('--count', default=10, help='Number of bibsets.')
@requires_db
def list(db, count):
    """
    List all the available ranking matrices.
    """
    ranking_matrices = db.query(RankingMatrix).order_by(
        RankingMatrix.created.desc()
    ).limit(count)

    click.echo(
        tabulate.tabulate(
            [
                [
                    rm.eid[:8],
                    rm.term_document_matrix.eid[:8],
                    rm.created.strftime('%b %d, %Y, %I:%M%p'),
                    rm.modified.strftime('%b %d, %Y, %I:%M%p'),
                ]
                for rm in ranking_matrices
            ],
            headers=[
                'Identifier',
                'Term document matrix',
                'Created at',
                'Updated at'
            ],
            tablefmt='rst',
        )
    )
    total = db.query(RankingMatrix).count()
    if count >= total:
        click.echo('Showing all the term document matrices.')
    else:
        click.echo(
            'Shwoing {count} out of {total} ranking matrices.'
            .format(count=count, total=total)
        )


@ranking.command()
@click.argument('target')
@requires_db
def delete(db, target):
    """
    Delete a given matrix and associated search engines.
    """
    try:
        ranking_matrix = db.query(RankingMatrix).filter(
            RankingMatrix.eid.like(target + '%')
        ).one()
    except sqlalchemy.orm.exc.NoResultFound:
        click.echo('Could not find a result matching {}'.format(target))
        return
    except sqlalchemy.orm.exc.MultipleResultsFound:
        click.echo('Found many results matching {}'.format(target))
        return

    click.echo(
        'I will delete the term document matrix {}.'
        .format(ranking_matrix.eid)
    )
    click.confirm('Do you want me to continue?', abort=True)
    db.delete(ranking_matrix)
