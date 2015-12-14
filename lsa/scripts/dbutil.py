import contextlib
import pymongo


# That global mongo client
MONGO_CLIENT = pymongo.MongoClient('localhost', 27017)


def collection_name(name):
    '''
    Prepends 'lsa-' to the given name.
    '''
    return 'lsa-' + name


@contextlib.contextmanager
def collection(name, dbname='program', delete=True):
    '''
    Returns a collection from the mongo database
    '''
    database = MONGO_CLIENT['lsa-' + dbname]
    records = database[name]
    if delete:
        records.delete_many({})
    records.create_index([('uuid', pymongo.ASCENDING)], unique=True)
    yield records
