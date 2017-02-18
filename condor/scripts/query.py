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
from condor.dbutil import requires_db
from condor.util import LanguageGuesser


def frequency(words, tokens):
    """
    Computes the frequency list of a list of tokens in a dense representation.

    :param list words: list of the words to look for
    :param list tokens: list of the tokens to count

    .. note:: this function applies a complete normalizer to the given tokens
    and guesses the language.
    """
    # word_dict = {word: pos for pos, word in enumerate(words)}
    language = LanguageGuesser().guess(' '.join(tokens))
    normalizer = CompleteNormalizer(language=language)
    frequency = collections.Counter(
        normalizer.apply_to(token)
        for token in tokens
    )
    return [frequency.get(word, 0) for word in words]


@click.command()
@click.argument('parameters', nargs=-1, required=True)
@click.option('--target', default=None, type=str,
              help='Ranking matrix to search')
@click.option('--limit', '-l', default=5,
              help='Results to show.')
@click.option('--show', '-s', type=str, multiple=True,
              help='Fields to show.')
@click.option('--verbose/--quiet', default=False,
              help='Be more verbose')
@requires_db
def query(db, parameters, limit, target, show, verbose):
    '''
    Queries the database using the given parameters, the model that this
    script will pick up to do the query is the latest available model.
    '''

    if verbose:
        click.echo('You queried: {}'.format(' '.join(parameters)))

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
    dot = numpy.dot(ranking_matrix, freq)
    norm_rank = numpy.linalg.norm(ranking_matrix, axis=1)
    norm_freq = numpy.linalg.norm(freq)
    cos = dot / (norm_rank * norm_freq)
    if verbose:
        click.echo('Your words are: {}'.format(words))
        click.echo('Your frequency is: {}'.format(freq))
        click.echo('Your cosines are: {}'.format(cos.shape))
        click.echo('Got a model with {} shape'.format(ranking_matrix.shape))

    ordered = reversed(sorted(zip(documents, cos), key=operator.itemgetter(1)))
    ordered = list(ordered)
    if 'title' not in show:
        show = ('title', ) + show
    for document, imp in ordered[:limit]:
        click.echo('')
        click.echo('With an importance of {}:'.format(imp))
        for field in show:
            try:
                click.echo(getattr(document, field))
            except:
                pass
