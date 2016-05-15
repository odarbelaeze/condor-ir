'''
This script aims to build the model for the current state of a database,
taking in all the present records.
'''

import collections
import hashlib
import itertools
import os
import sys

import click
import numpy
import scipy

from lsa.dbutil import session
from lsa.models import (
    BibliographySet,
    TermDocumentMatrix,
    RankingMatrix
)
from lsa.normalize import CompleteNormalizer


def get_tokens(record, fields=None, list_fields=None):
    fields = fields or ['title', 'description', ]
    list_fields = list_fields or ['keywords', ]
    tokens = []
    for field in fields:
        tokens.extend(record.get(field, '').split())
    for field in list_fields:
        value = record.get(field, '{""}')
        if value == '{""}':
            continue
        tokens.extend(value[1:-1].split(','))
    return tokens


def raw_data(bib):
    normalizer = CompleteNormalizer(language=bib.language)
    return [normalizer.apply_to(token) for token in get_tokens(bib.__dict__)]


def word_set(bibset):
    def words():
        for bib in bibset.bibliographies:
            yield raw_data(bib)
    return sorted(set(itertools.chain.from_iterable(words())))


def records(bibset):
    for bib in bibset.bibliographies:
        yield bib.eid


def matrix(bibset, words):
    word_dict = {word: pos for pos, word in enumerate(words)}
    for ind, bib in enumerate(bibset.bibliographies):
        raw = list(raw_data(bib))
        frequency = collections.Counter(raw)
        for word, freq in frequency.items():
            yield ind, word_dict[word], freq


@click.command()
@click.option('--target', default=None, type=str)
@click.option('--verbose/--quiet', default=False,
              help='Be more verbose')
def lsamodel(target, verbose):
    '''
    Creates a model for all the records presentin in the record collection of
    the database specified in `dbname`.

    'lsa-' will be prepended to the database name provided thorugh the
    `--dbname` flag.
    '''

    db = session()
    if target is None:
        bibset = db.query(BibliographySet).order_by('created desc').first()
    else:
        query = db.query(BibliographySet)
        query = query.filter(BibliographySet.eid.like(target + '%'))
        bibset = query.first()

    if bibset is None:
        click.echo('Please create a bibset first')
        sys.exit(1)

    click.echo('I will generate a model for the {} bibset...'.format(
        bibset.eid))

    words = word_set(bibset)
    nwords = len(words)
    click.echo('I found {} unique word toquens in the database...'.format(
        len(words)))

    ndocs = len(bibset.bibliographies)
    click.echo(
        'I found {} unique documents toquens in the database...'.format(
            ndocs
        )
    )

    frequency = numpy.zeros((ndocs, nwords), dtype=int)
    for row, col, freq in matrix(bibset, words):
        frequency[row, col] = freq

    if verbose:
        nwords, nrecs = matrix.shape
        click.echo('I\'ve built the frequency matrix with the folowing traits')
        click.echo('Number of records: {}'.format(nrecs))
        click.echo('Number of words: {}'.format(nwords))

    # U, S, V = scipy.sparse.linalg.svds(sparse, 562)
    U, S, V = scipy.linalg.svd(frequency, full_matrices=False)

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

    if not os.path.exists('matrices'):
        os.mkdir('matrices')

    matrix_hash = hashlib.sha1(
        '{}{}{}{}'.format(bibset.eid, bibset.modified, ndocs, nwords)
        .encode()
    ).hexdigest()

    matrix_filename = os.path.join('matrices', '{}.npy'.format(matrix_hash))
    click.echo(
        'Storing the term document matrix at {}'
        .format(matrix_filename)
    )
    numpy.save(matrix_filename, matrix)

    if not os.path.exists('term_lists'):
        os.mkdir('term_lists')

    term_list_path = os.path.join('term_lists', '{}.txt'.format(matrix_hash))
    click.echo(
        'Storing the term list at {}'
        .format(term_list_path)
    )
    with open(term_list_path, 'w') as file:
        file.write('\n'.join(words))

    if not os.path.exists('models'):
        os.mkdir('models')

    model_hash = hashlib.sha1(
        '{}{}{}{}lsa'.format(bibset.eid, bibset.modified, ndocs, nwords)
        .encode()
    ).hexdigest()

    model_filename = os.path.join('models', '{}.npy'.format(model_hash))
    click.echo(
        'Storing the ranking matrix at {}'
        .format(model_filename)
    )
    numpy.save(model_filename, acoted)
    td_matrix = TermDocumentMatrix(
        bibliography_options='',
        processing_options=str(CompleteNormalizer.__mro__),
        term_list_path=term_list_path,
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
