"""
Implements the condor matrix commands to create term document matrices from
bibsets.
"""

import click
import sqlalchemy
import sys
import tabulate

from condor.dbutil import requires_db, one_or_latest
from condor.models import TermDocumentMatrix, RankingMatrix


@click.group()
def ranking():
    """
    Term document matrix related commands.
    """
    pass


@ranking.command()
@click.option('--target', default=None, type=str,
              help='Document set to work with')
@click.option('--covariance', default=0.8,
              help='Default covariance to keep in an lsa model')
@click.option('--verbose/--quiet', default=False,
              help='Be more verbose')
@requires_db
def create(database, target, covariance, verbose):
    """
    Create a new term document matrix.
    """
    td_matrix = one_or_latest(database, TermDocumentMatrix, target)
    if td_matrix is None:
        click.echo('Please create a matrix first')
        sys.exit(1)

    if verbose:
        click.echo(
            'I will generate a ranking for the {} term doc matrix.'.format(
                td_matrix.eid
            )
        )

    ranking_matrix = RankingMatrix.lsa_from_term_document_matrix(
        term_document_matrix=td_matrix,
        covariance=covariance,
    )
    database.add(ranking_matrix)

    click.secho('Done!', fg='green')


@ranking.command('list')
@click.option('--count', default=10, help='Number of bibsets.')
@requires_db
def list_ranking_matrices(database, count):
    """
    List all the available ranking matrices.
    """
    ranking_matrices = RankingMatrix.list(database, count)
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
    total = RankingMatrix.count(database)
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
def delete(database, target):
    """
    Delete a given matrix and associated search engines.
    """
    try:
        ranking_matrix = database.query(RankingMatrix).filter(
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
    database.delete(ranking_matrix)
