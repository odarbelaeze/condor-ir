import bisect
import collections
import contextlib
import glob
import itertools

import numpy
import pymongo
import scipy.sparse
import scipy.linalg

from xml.dom import minidom
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

from matplotlib import pyplot as plt


STOPWORDS = sorted(stopwords.words())
# http://www.talkpythontome.com/episodes/show/2/python-and-mongodb
# Don't be afraid of creating a global for the mongo client
MONGO_CLIENT = pymongo.MongoClient('localhost', 27017)
STEMER = SnowballStemmer('spanish')


class Record(object):

    def __init__(self, dom_element):
        self.dom_element = dom_element

    @property
    def title(self):
        title = self.dom_element.getElementsByTagName('lom:title').item(0)
        if title is None:
            return ''
        return title.firstChild.nodeValue

    @property
    def keywords(self):
        keywords = self.dom_element.getElementsByTagName('lom:keyword')
        if keywords.length == 0:
            return ''
        return ' '.join([keyword.firstChild.nodeValue
                         for keyword in keywords])

    @property
    def description(self):
        description = self.dom_element.getElementsByTagName('lom:description')
        description = description.item(0)
        if description is None:
            return ''
        return description.firstChild.nodeValue

    @property
    def location(self):
        location = self.dom_element.getElementsByTagName('lom:location').item(0)
        if location is None:
            return ''
        return location.firstChild.nodeValue

    @property
    def xml(self):
        return self.dom_element.toxml()

    @property
    def metadata(self):
        return {
            'title': self.title,
            'keywords': self.keywords,
            'description': self.description,
            'location': self.location,
            'xml': self.xml,
        }

    def raw_data(self, fields=None):
        return raw_data(self.metadata, fields)


def is_stopword(word):
    i = bisect.bisect_left(STOPWORDS, word.lower())
    if i < len(STOPWORDS) and word.lower() == STOPWORDS[i]:
        return True
    return False


def is_valid(word):
    return not is_stopword(word) and not word.isspace() and word.isalnum()


def normalize(word):
    return STEMER.stem(word.lower())


def raw_data(record, interest_fields=None):
    _interest_fields = interest_fields or ['title', 'keywords', 'description']
    tokens = []
    for key in _interest_fields:
        key_tokens = word_tokenize(record[key], language='spanish')
        tokens.extend(key_tokens)
    return filter(is_valid, map(normalize, tokens))


def metadata(filename):
    dom = minidom.parse(filename)
    for dom_element in dom.getElementsByTagName('record'):
        record = Record(dom_element)
        yield record.metadata


@contextlib.contextmanager
def collection(dbname='lsa-froac', delete=True):
    database = MONGO_CLIENT[dbname]
    records = database['records']
    if delete:
        records.delete_many({})
    yield records


def word_set():
    def words():
        with collection(delete=False) as records:
            for record in records.find():
                yield raw_data(record)
    return sorted(set(itertools.chain.from_iterable(words())))


def matrix(words):

    word_dict = {word: pos for pos, word in enumerate(words)}

    with collection(delete=False) as records:
        for ind, record in enumerate(records.find()):
            raw = list(raw_data(record))
            frequency = collections.Counter(raw)
            for word, freq in frequency.items():
                yield ind, word_dict[word], freq


def main():
    with collection() as records:
        for filename in glob.glob('data/**/*.xml'):
            records.insert_many(
                list(metadata(filename)))

    words = word_set()
    mat = matrix(words)
    rowid, colid, freq = zip(*mat)
    sparse = scipy.sparse.csr_matrix((freq, (rowid, colid)), dtype='f').T
    nwords, nrecs = sparse.shape

    print('Number of records: ', nrecs)
    print('Number of words: ', nwords)
    print('sparcity: %f' % (sparse.nnz / (nwords * nrecs) * 100))

    tf = sparse.toarray()
    gf = numpy.sum(tf, axis=1)
    pij = (tf.T / gf).T
    _pij_ = pij.copy()
    _pij_[pij == 0.0] = 1   # Log safe pij

    log = numpy.log(tf + 1)
    entropy = numpy.sum(pij * numpy.log(_pij_), axis=1) / numpy.log(nrecs) + 1

    termdoc = (log.T * entropy).T

    # U, S, V = scipy.sparse.linalg.svds(sparse, 562)
    U, S, V = scipy.linalg.svd(termdoc, full_matrices=False)

    ss = S / numpy.sum(S)
    ss = numpy.cumsum(ss)

    k = numpy.sum(ss < 0.8)

    print(S.sum())

    print('U shape: ', U.shape)
    print('S shape: ', S.shape)
    print('V shape: ', V.shape)

    acoted = numpy.dot(numpy.diag(S[:k]), V[:k, :])
    acoted = numpy.dot(U[:, :k], acoted)
    print(acoted.shape)

    plt.matshow(termdoc, cmap=plt.cm.gray)
    plt.matshow(acoted, cmap=plt.cm.gray)

    x = numpy.sum(termdoc, axis=1)
    plt.figure()
    plt.hist(x, bins=70)
    plt.show()


if __name__ == '__main__':
    main()
