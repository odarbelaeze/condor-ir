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
    ranking_matrix = find_one(db, RankingMatrix, target)
    bibliography_set = ranking_matrix.term_document_matrix.bibliography_set
    queries = bibliography_set.queries
    universe = set(d.eid for d in bibliography_set.bibliographies)

    for query in queries:
        results = ranking_matrix.query(query.query_string.split(), limit=limit)
        experiment = set(r.eid for r, _ in results)
        truth = set(r.bibliography.eid for r in query.results)
        false_negatives = truth.difference(experiment)
        true_positives = truth.intersection(experiment)
        false_positives = experiment.difference(truth)
        true_negatives = universe.difference(truth.union(experiment))
        print(
            query.query_string,
            '\n',
            'FN', len(false_negatives),
            'TP', len(true_positives),
            'FP', len(false_positives),
            'TN', len(true_negatives),
            '\n',
        )
