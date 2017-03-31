"""
This script aims to build the model for the current state of a database,
taking in all the present records.
"""

import sys

import click

from condor.dbutil import requires_db, one_or_latest
from condor.models import BibliographySet, TermDocumentMatrix, RankingMatrix


@click.group()
def model():
    """
    Model shortcut to handle both a matrix and a ranking
    at the same time.
    """
    pass


@model.command()
@click.option('--target', default=None, type=str,
              help='Bibliography set to work with')
@click.option('--regularise', is_flag=True,
              help='Regularise the term document matrix on creation')
@click.option('--covariance', default=0.8,
              help='Default covariance to keep in an lsa model')
@click.option('--field', '-f', 'fields', multiple=True, type=str, default=None,
              help='Use these fields on matrix creation.')
@click.option('--verbose/--quiet', default=False,
              help='Be more verbose')
@requires_db
def create(db, target, regularise, covariance, fields, verbose):
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
        bibliography_set, regularise=regularise, fields=fields
    )
    db.add(td_matrix)
    db.flush()

    ranking_matrix = RankingMatrix.lsa_from_term_document_matrix(
        term_document_matrix=td_matrix,
        covariance=covariance,
    )
    db.add(ranking_matrix)
    click.secho('Done!', fg='green')
