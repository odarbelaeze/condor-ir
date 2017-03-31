"""
This script aims to build the model for the current state of a database,
taking in all the present records.
"""

import os
import sys

import click
import numpy

from condor.dbutil import requires_db
from condor.builders.ranking import build_lsa_ranking
from condor.models import BibliographySet, TermDocumentMatrix, RankingMatrix
from condor.config import MODEL_PATH


@click.group()
def model():
    """
    Model shortcut to handle both a matrix and a ranking
    at the same time.
    """
    pass


@model.command()    # noqa
@click.option('--target', default=None, type=str,
              help='Bibliography set to work with')
@click.option('--regularise', is_flag=True,
              help='Regularise the term document matrix on creation')
@click.option('--verbose/--quiet', default=False,
              help='Be more verbose')
@requires_db
def create(db, target, regularise, verbose):
    """
    Creates a ranking matrix and a lsa model for the specified bibset.
    """

    bibliography_set = one_or_latest(db, BibliographySet, target)
    if bibliography_set is None:
        click.echo('Please create a bibset first')
        sys.exit(1)

    if verbose:
        click.echo('I will generate a model for the {} bibset...'.format(
            bibliography_set.eid))

    td_matrix = TermDocumentMatrix.from_bibliography_set(
        bibliography_set, regularise=regularise
    )

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

    td_matrix.ranking_matrices = [
        RankingMatrix(
            kind='lsa',
            build_options=ranking_result.options,
            ranking_matrix_path=model_filename,
        )
    ]

    db.add(td_matrix)
