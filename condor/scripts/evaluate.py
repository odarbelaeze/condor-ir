"""
Scripts to evaluate rankins based on ground truth databases.
"""

import collections
import json

import click
import numpy

from condor.dbutil import requires_db, find_one
from condor.models.ranking_matrix import RankingMatrix


PerformanceResult = collections.namedtuple(
    'PerformanceResult',
    [
        'true_positives',
        'true_negatives',
        'false_positives',
        'false_negatives',
        'precision',
        'recall',
        'f1_score',
    ]
)


@click.command()
@click.argument('target')
@click.option('--limit', '-l', default=None, type=int,
              help='limit the number of results to use.')
@click.option('--cosine', '-c', default=None, type=float,
              help='limit the query by cosine.')
@click.option('--words', '-w', default=None, type=int,
              help='limit the number of words in the query')
@click.option('--output', '-o', type=click.File('w'),
              help='export a detailed performance report')
@click.option('--tabular', '-t', is_flag=True,
              help='show tabular output')
@requires_db
def evaluate(db, target, limit, cosine, words, tabular, output):
    """
    Evaluates a target search engine, the search engine needs to be associated
    to some queries in order to be evaluated, this command mainly returns
    precision and recall values for the different queries and an average of
    these values at the end.
    """
    ranking_matrix = find_one(db, RankingMatrix, target)
    bibliography = ranking_matrix.term_document_matrix.bibliography
    queries = bibliography.queries
    universe = set(d.eid for d in bibliography.documents)

    # We'll perform all the queries and  do a mean of the f1 score

    performance_results = {}

    for query in queries:
        if words is not None and len(query.query_string.split()) != words:
            continue
        results = ranking_matrix.query(
            query.query_string.split(), limit=limit, cosine=cosine)
        experiment = set(r.eid for r, _ in results)
        truth = set(r.document.eid for r in query.results)
        false_negatives = truth.difference(experiment)
        true_positives = truth.intersection(experiment)
        false_positives = experiment.difference(truth)
        true_negatives = universe.difference(truth.union(experiment))

        # Validate precision
        if len(true_positives) + len(false_positives) > 0:
            precision = len(true_positives) / \
                (len(true_positives) + len(false_positives))
        else:
            precision = None

        # Validate recall this might never happen
        if len(true_positives) + len(false_negatives) > 0:
            recall = len(true_positives) / \
                (len(true_positives) + len(false_negatives))
        else:
            recall = None

        if precision is not None and recall is not None and precision + recall > 0:
            f1_score = 2 * precision * recall / (precision + recall)
        else:
            f1_score = None

        performance_results[query.query_string] = PerformanceResult(
            false_negatives=len(false_negatives),
            true_positives=len(true_positives),
            false_positives=len(false_positives),
            true_negatives=len(true_negatives),
            precision=precision,
            recall=recall,
            f1_score=f1_score,
        )

    averages = {
        metric: numpy.mean([
            getattr(result, metric)
            for result in performance_results.values()
            if getattr(result, metric) is not None
        ])
        for metric in ('precision', 'recall', 'f1_score')
    }

    if output:
        json.dump({
            'parameters': {
                'target': ranking_matrix.eid,
                'queries': len(performance_results),
                'cosine': cosine,
                'limit': limit,
            },
            'averages': averages,
            'results': {
                q: res._asdict()
                for q, res in performance_results.items()
            },
        }, output, indent=2)

    if tabular:
        click.echo('{param} {results}'.format(
            param=limit or cosine or 10,
            results=' '.join([str(a) for a in averages.values()])
        ))
    else:
        click.echo(json.dumps(averages, indent=2))
