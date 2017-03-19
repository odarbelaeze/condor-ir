import click

from condor.dbutil import requires_db, find_one
from condor.models.ranking_matrix import RankingMatrix


@click.command()
@click.argument('target')
@click.option('--limit', '-l', default=10,
              help='limit the number of results to use.')
@requires_db
def evaluate(db, target, limit):
    """
    Evaluates a target search engine, the search engine needs to be associated
    to some queries in order to be evaluated, this command mainly returns
    precision and recall values for the different queries and an average of
    these values at the end.
    """
    rankin_matrix = find_one(db, RankingMatrix, target)
    queries = rankin_matrix.term_document_matrix.bibliography_set.queries

    for query in queries:
        results = rankin_matrix.query(query.query_string.split(), limit=limit)
        print(results)
