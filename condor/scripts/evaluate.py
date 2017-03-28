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
    ]
)


@click.command()
@click.argument('target')
@click.option('--limit', '-l', default=10,
              help='limit the number of results to use.')
@click.option('--output', '-o', type=click.File('w'),
              help='export a detailed performance report')
@requires_db
def evaluate(db, target, limit, output):
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

    # We'll perform all the queries and  do a mean of the f1 score

    performance_results = {}

    for query in queries:
        results = ranking_matrix.query(query.query_string.split(), limit=limit)
        experiment = set(r.eid for r, _ in results)
        truth = set(r.bibliography.eid for r in query.results)
        false_negatives = truth.difference(experiment)
        true_positives = truth.intersection(experiment)
        false_positives = experiment.difference(truth)
        true_negatives = universe.difference(truth.union(experiment))

        # Validate precision
        if len(true_positives) + len(false_positives) > 0:
            precision = len(true_positives) / \
                (len(true_positives) + len(false_positives))
        else:
            precision = 0.0

        # Validate recall this might never happen
        if len(true_positives) + len(false_negatives) > 0:
            recall = len(true_positives) / \
                (len(true_positives) + len(false_negatives))
        else:
            recall = 0.0

        performance_results[query.query_string] = PerformanceResult(
            false_negatives=len(false_negatives),
            true_positives=len(true_positives),
            false_positives=len(false_positives),
            true_negatives=len(true_negatives),
            precision=precision,
            recall=recall,
        )

    mean_f1_score = numpy.mean([
        2 * result.precision * result.recall / (result.precision + result.recall)
        for result in performance_results.values()
        if result.precision + result.recall > 0
    ])

    if output:
        json.dump({
            q: res._asdict()
            for q, res in performance_results.items()
        }, output, indent=2)

    click.echo(mean_f1_score)
