"""
Uses the latest model to query the database for the most important documents
according to lsa.
"""

import sys

import click

from condor.dbutil import requires_db, one_or_latest
from condor.models import RankingMatrix


@click.command()
@click.argument('parameters', nargs=-1, required=True)
@click.option('--target', default=None, type=str,
              help='Ranking matrix to search')
@click.option('--limit', '-l', default=None, type=int,
              help='Results to show.')
@click.option('--cosine', '-c', default=None, type=float,
              help='Max cosine to show.')
@click.option('--show', '-s', type=str, multiple=True,
              help='Fields to show.')
@click.option('--verbose/--quiet', default=False,
              help='Be more verbose')
@requires_db
def query(database, parameters, limit, cosine, target, show, verbose):
    """
    Queries the database using the given parameters, the model that this
    script will pick up to do the query is the latest available model.
    """

    if verbose:
        click.echo('You queried: {}'.format(' '.join(parameters)))

    ranking_matrix = one_or_latest(database, RankingMatrix, target)

    if ranking_matrix is None:
        click.echo('Please create a ranking first')
        sys.exit(1)

    click.echo('I will query the ranking for the {} ranking...'.format(
        ranking_matrix.eid))

    results = ranking_matrix.query(parameters, limit=limit, cosine=cosine)

    if not results:
        click.echo('No result found for: {}'.format(' '.join(parameters)))

    if 'title' not in show:
        show = ('title', ) + show
    for document, imp in results:
        click.echo('')
        click.echo('With a score of {}:'.format(imp))
        for field in show:
            try:
                click.echo(getattr(document, field))
            except AttributeError:
                pass
