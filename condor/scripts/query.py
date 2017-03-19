'''
Uses the latest model to query the database for the most important documents
according to lsa.
'''

import operator
import sys

import click
import numpy

from condor.dbutil import requires_db
from condor.models import RankingMatrix
from condor.util import frequency


@click.command()
@click.argument('parameters', nargs=-1, required=True)
@click.option('--target', default=None, type=str,
              help='Ranking matrix to search')
@click.option('--limit', '-l', default=5,
              help='Results to show.')
@click.option('--show', '-s', type=str, multiple=True,
              help='Fields to show.')
@click.option('--verbose/--quiet', default=False,
              help='Be more verbose')
@requires_db
def query(db, parameters, limit, target, show, verbose):
    '''
    Queries the database using the given parameters, the model that this
    script will pick up to do the query is the latest available model.
    '''

    if verbose:
        click.echo('You queried: {}'.format(' '.join(parameters)))

    if target is None:
        ranking = db.query(RankingMatrix).order_by(
            RankingMatrix.created.desc()
        ).first()
    else:
        query = db.query(RankingMatrix)
        query = query.filter(RankingMatrix.eid.like(target + '%'))
        ranking = query.first()

    if ranking is None:
        click.echo('Please create a ranking first')
        sys.exit(1)

    click.echo('I will query the ranking for the {} bibset...'.format(
        ranking.eid))

    results = ranking.query(parameters, limit=limit)

    if not results:
        click.echo('No result found for: {}'.format(' '.join(parameters)))

    if 'title' not in show:
        show = ('title', ) + show
    for document, imp in results:
        click.echo('')
        click.echo('With an importance of {}:'.format(imp))
        for field in show:
            try:
                click.echo(getattr(document, field))
            except:
                pass
