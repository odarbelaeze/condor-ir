import contextlib

import click
import pymongo


# That global mongo client
MONGO_CLIENT = pymongo.MongoClient('localhost', 27017)


@contextlib.contextmanager
def collection(dbname='froac', delete=True):
    database = MONGO_CLIENT['lsa-' + dbname]
    records = database['records']
    if delete:
        records.delete_many({})
    yield records


@click.command()
@click.argument('pattern')
@click.option('--xml', 'kind', flag_value='xml', default=True)
@click.option('--isi', 'kind', flag_value='isi')
def lsapopulate(pattern, kind):
    click.echo(pattern)
    click.echo(kind)
    click.echo('looking for {} records in files matching {}'.format(kind, pattern))
