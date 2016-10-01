'''
This script aims to build the model for the current state of a database,
taking in all the present records.
'''

import hashlib
import os
import sys

import click
import numpy

from condor.dbutil import session
from condor.builders.matrix import build_matrix
from condor.models import (
    BibliographySet,
    TermDocumentMatrix,
    RankingMatrix
)
from condor.config import (
    TERM_LIST_PATH,
    MATRIX_PATH,
    MODEL_PATH,
)


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
@click.option('--verbose/--quiet', default=False,
              help='Be more verbose')
def create(target, verbose):
    '''
    Creates a ranking matrix and a lsa model for the specified bibset.
    '''

    db = session()
    if target is None:
        bibset = db.query(BibliographySet).order_by(
            BibliographySet.created.desc()
        ).first()
    else:
        query = db.query(BibliographySet)
        query = query.filter(BibliographySet.eid.like(target + '%'))
        bibset = query.first()

    if bibset is None:
        click.echo('Please create a bibset first')
        sys.exit(1)

    click.echo('I will generate a model for the {} bibset...'.format(
        bibset.eid))

    words, frequency, options = build_matrix(bibset)
    nwords, nrecs = frequency.shape

    if verbose:
        click.echo('I\'ve built the frequency matrix with the folowing traits')
        click.echo('Number of records: {}'.format(nrecs))
        click.echo('Number of words: {}'.format(nwords))

    U, S, V = numpy.linalg.svd(frequency, full_matrices=False)
    ss = S / numpy.sum(S)
    ss = numpy.cumsum(ss)

    # Keep 80% of the covariance
    k = numpy.sum(ss < 0.8)

    acoted = numpy.dot(numpy.diag(S[:k]), V[:k, :])
    acoted = numpy.dot(U[:, :k], acoted)

    if verbose:
        nwords, nrecs = acoted.shape
        click.echo('I\'ve removed noise from the freq mat...')
        click.echo('Number of records: {}'.format(nrecs))
        click.echo('Number of words: {}'.format(nwords))

    matrix_hash = hashlib.sha1(
        '{}{}{}{}'.format(bibset.eid, bibset.modified, nrecs, nwords)
        .encode()
    ).hexdigest()
    matrix_filename = os.path.join(MATRIX_PATH, '{}.npy'.format(matrix_hash))
    click.echo(
        'Storing the term document matrix at {}'
        .format(matrix_filename)
    )
    numpy.save(matrix_filename, frequency)

    term_list_filename = os.path.join(
        TERM_LIST_PATH, '{}.txt'.format(matrix_hash)
    )
    click.echo(
        'Storing the term list at {}'.format(TERM_LIST_PATH)
    )
    with open(term_list_filename, 'w') as file:
        file.write('\n'.join(words))

    model_hash = hashlib.sha1(
        '{}{}{}{}condor'.format(bibset.eid, bibset.modified, nrecs, nwords)
        .encode()
    ).hexdigest()
    model_filename = os.path.join(MODEL_PATH, '{}.npy'.format(model_hash))
    click.echo(
        'Storing the ranking matrix at {}'
        .format(model_filename)
    )
    numpy.save(model_filename, acoted)
    td_matrix = TermDocumentMatrix(
        bibliography_options='',
        processing_options=options,
        term_list_path=term_list_filename,
        tdidf_matrix_path=matrix_filename,
    )
    td_matrix.bibliography_set = bibset
    td_matrix.ranking_matrices = [
        RankingMatrix(
            kind='lsa',
            build_options='',
            ranking_matrix_path=model_filename,
        )
    ]
    db.add(td_matrix)
    db.commit()
