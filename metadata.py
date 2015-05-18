import bisect
import glob
import contextlib

import pymongo

from xml.dom import minidom
from nltk.corpus import stopwords


STOPWORDS = stopwords.words()
# http://www.talkpythontome.com/episodes/show/2/python-and-mongodb
# Don't be afraid of creating a global for the mongo client
MONGO_CLIENT = pymongo.MongoClient('localhost', 27017)


def title(record):
    title = record.getElementsByTagName('lom:title').item(0)
    if title is None:
        return ''
    return title.firstChild.nodeValue


def keywords(record):
    keywords = record.getElementsByTagName('lom:keyword')
    if keywords.length == 0:
        return ''
    return ' '.join([keyword.firstChild.nodeValue
                     for keyword in keywords])


def description(record):
    description = record.getElementsByTagName('lom:description').item(0)
    if description is None:
        return ''
    return description.firstChild.nodeValue


def metadata(filename):
    dom = minidom.parse(filename)
    record_id = -1
    for record in dom.getElementsByTagName('record'):
        record_id += 1
        yield {
            'title': title(record),
            'keywords': keywords(record),
            'description': description(record),
            'raw': record.toxml(),
            'id': record_id,
        }


def is_stopword(word):
    return bisect.bisect_left(STOPWORDS, word) < len(STOPWORDS)
    # return word in STOPWORDS


def raw_data(record, interest_fields=None):
    _interest_fields = interest_fields or ['title', 'keywords', 'description']
    tokens = []
    for key in _interest_fields:
        tokens.extend(record[key].split(' '))     # this will change
    return filter(is_stopword, tokens)


@contextlib.contextmanager
def collection(delete=True):
    database = MONGO_CLIENT['lsa-froac']
    records = database['records']
    records.create_index([('id', pymongo.ASCENDING, ), ])
    if delete:
        records.delete_many({})
    yield records


def main():
    with collection() as records:
        for filename in glob.glob('data/*.xml'):
            records.insert_many(
                list(metadata(filename)))

    with collection(delete=False) as records:
        for record in records.find():
            print(' '.join(raw_data(record)))

if __name__ == '__main__':
    main()
