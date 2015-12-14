"""
This script aims to build the model for the current state of a database,
taking in all the present records.
"""

import collections
import datetime
import itertools
import os
import uuid

import click
import numpy
import scipy

from lsa.util import normalize

from .dbutil import collection
from .dbutil import collection_name


def raw_data(record):
    return map(normalize, record['tokens'])


def word_set(dbname):
    def words():
        with collection('records', dbname=dbname, delete=False) as records:
            for record in records.find():
                yield raw_data(record)
    return sorted(set(itertools.chain.from_iterable(words())))


def records(dbname):
    with collection('records', dbname=dbname, delete=False) as records:
        for record in records.find():
            yield record["_id"]


def matrix(dbname, words):
    word_dict = {word: pos for pos, word in enumerate(words)}
    with collection('records', dbname=dbname, delete=False) as records:
        for ind, record in enumerate(records.find()):
            raw = list(raw_data(record))
            frequency = collections.Counter(raw)
            for word, freq in frequency.items():
                yield ind, word_dict[word], freq


@click.command()
@click.option('--dbname', default='program',
              help='Name of the mongo database to use to store the records')
@click.option('--verbose/--quiet', default=False,
              help='Be more verbose')
def lsamodel(dbname, verbose):
    '''
    Creates a model for all the records presentin in the record collection of
    the database specified in `dbname`.

    'lsa-' will be prepended to the database name provided thorugh the
    `--dbname` flag.
    '''

    click.echo("I will generate a model for the {} database...".format(
        collection_name(dbname)))

    words = word_set(dbname)
    click.echo('I found {} unique word toquens in the database...'.format(
        len(words)))

    mat = matrix(dbname, words)
    rowid, colid, freq = zip(*mat)
    sparse = scipy.sparse.csr_matrix((freq, (rowid, colid)), dtype='f').T

    if verbose:
        nwords, nrecs = sparse.shape
        click.echo('I\'ve built the frequency matrix with the folowing traits:')
        click.echo('Number of records: {}'.format(nrecs))
        click.echo('Number of words: {}'.format(nwords))
        click.echo('sparcity: {:0.2f}%'.format(
            sparse.nnz / (nwords * nrecs) * 100))

    # U, S, V = scipy.sparse.linalg.svds(sparse, 562)
    U, S, V = scipy.linalg.svd(sparse.todense(), full_matrices=False)

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

    if not os.path.exists('models'):
        os.mkdir('models')

    model_uuid = '{}'.format(uuid.uuid4())
    model_filename = os.path.join('models', '{}.npy'.format(model_uuid))
    click.echo('Storing the model at {}'.format(model_filename))
    numpy.save(model_filename, acoted)

    with collection('models', dbname=dbname, delete=False) as models:
        models.insert_one({
            'uuid': model_uuid,
            'file': os.path.abspath(model_filename),
            'words': words,
            'docs': list(records(dbname)),
            'created_at': datetime.datetime.now(),
        })
