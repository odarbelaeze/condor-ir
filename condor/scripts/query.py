'''
Uses the latest model to query the database for the most important documents
according to lsa.
'''

import collections
import operator
import sys

import click
import numpy

from condor.normalize import CompleteNormalizer
from condor.models import RankingMatrix
from condor.dbutil import session, requires_db


def frequency(words, tokens):
    # word_dict = {word: pos for pos, word in enumerate(words)}
    normalizer = CompleteNormalizer()
    frequency = collections.Counter(
        normalizer.apply_to(token)
        for token in tokens
    )
    return [frequency.get(word, 0) for word in words]


@click.command()
@click.argument('parameters', nargs=-1, required=True)
@click.option('--target', default=None, type=str)
@click.option('--verbose/--quiet', default=False,
              help='Be more verbose')
@requires_db
def query(parameters, target, verbose):
    '''
    Queries the database using the given parameters, the model that this
    script will pick up to do the query is the latest available model.
    '''

    click.echo('You queried: {}'.format(' '.join(parameters)))

    db = session()
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

    ranking_matrix = numpy.load(ranking.ranking_matrix_path)

    words_filename = ranking.term_document_matrix.term_list_path
    with open(words_filename, 'r') as words_file:
        words = words_file.read().split('\n')

    freq = frequency(words, parameters)
    documents = ranking.term_document_matrix.bibliography_set.bibliographies
    cos = numpy.dot(ranking_matrix, freq)
    if verbose:
        click.echo('Your words are: {}'.format(words))
        click.echo('Your frequency is: {}'.format(freq))
        click.echo('Your cosines are: {}'.format(cos.shape))
        click.echo('Got a model with {} shape'.format(ranking_matrix.shape))

    ordered = reversed(sorted(zip(documents, cos), key=operator.itemgetter(1)))
    ordered = list(ordered)
    for document, imp in ordered[:3]:
        click.echo('')
        click.echo('With an importance of {}:'.format(imp))
        click.echo(document.title)
        click.echo(document.description)
