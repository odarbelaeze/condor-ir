'''
Uses the latest model to query the database for the most important documents
according to lsa.
'''

import collections
import operator

import click
import pymongo
import numpy

from bson.objectid import ObjectId

from lsa.util import normalize as preprocess

from .dbutil import collection


def frequency(words, tokens):
    # word_dict = {word: pos for pos, word in enumerate(words)}
    frequency = collections.Counter(map(preprocess, tokens))
    return [frequency.get(word, 0) for word in words]


@click.command()
@click.argument('parameters', nargs=-1, required=True)
@click.option('--dbname', default='program',
              help='Name of the mongo database to use to store the records')
@click.option('--verbose/--quiet', default=False,
              help='Be more verbose')
def lsaquery(parameters, dbname, verbose):
    click.echo('You queried: {}'.format(' '.join(parameters)))
    with collection('models', dbname=dbname, delete=False) as models:
        model = models.find().sort('created_at', pymongo.DESCENDING).limit(1)[0]
        if verbose:
            click.echo(model['created_at'])
    ranking = numpy.load(model['file'])
    words = model['words']
    freq = frequency(words, parameters)
    documents = model['docs']
    cos = numpy.dot(freq, ranking)
    if verbose:
        click.echo('Your words are: {}'.format(words))
        click.echo('Your frequency is: {}'.format(freq))
        click.echo('Your cosines are: {}'.format(cos.shape))
        click.echo('Got a model with {} shape'.format(ranking.shape))

    ordered = reversed(sorted(zip(documents, cos), key=operator.itemgetter(1)))
    ordered = list(ordered)
    with collection('records', dbname=dbname, delete=False) as records:
        for document, imp in ordered[:3]:
            record = records.find_one({'_id': ObjectId(document)})
            click.echo('')
            click.echo('With an importance of {}:'.format(imp))
            click.echo(record['title'])
            click.echo(record['description'])
