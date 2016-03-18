'''
Utils to work with a mongo database, it contains a global connection to the
database so that a new one is not created with every request which is a huge
overhead. Furthermore it has a tool to use a pymongo collection as a context
manager.
'''

import contextlib
import pymongo


# That global mongo client
MONGO_CLIENT = pymongo.MongoClient('localhost', 27017)


def collection_name(name):
    '''
    Prepends 'lsa-' to the given name, so that all collections for the lsa
    program have consistent names.
    '''
    return 'lsa-' + name


@contextlib.contextmanager
def collection(name, dbname='program', delete=True):
    '''
    Yields a mongo collection with name the given name in the specified
    database it has the advantage of not having to create the collection
    everywhere in the program.

    :param name: name of the collection
    :param dbname: name of the database to get the collection from
    :param delete: either delete the content of the collection or not
    :type name: str like
    :type dbname: str like
    :type delete: bool
    :return: collection as a context manager
    :rtype: ContextManager
    '''
    database = MONGO_CLIENT['lsa-' + dbname]
    records = database[name]
    if delete:
        records.delete_many({})
    records.create_index([('uuid', pymongo.ASCENDING)], unique=True)
    yield records
