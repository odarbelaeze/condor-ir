import bisect
import collections
import functools
import string

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


# STOPWORDS = {k: k for k in stopwords.words()}
STOPWORDS = sorted(stopwords.words())

# This is a little STEMER
STEMER = SnowballStemmer('spanish')

# Translation table to get rid of punctuation
PUNCTUATION = str.maketrans(dict.fromkeys(string.punctuation))


def xml_to_text(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            return ''
        return result.firstChild.nodeValue
    return inner


def gen_to_list(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return list(func(*args, **kwargs))
    return inner


def isi_text_to_dic(text):
    fields = collections.defaultdict(list)
    curr = ""
    for line in text.split('\n'):
        name = line[:2]
        value = line[3:]
        if not name.isspace():
            curr = name
        if not curr.isspace():
            fields[curr].append(value)
    return fields


def is_stopword(word):
    # TODO A hsh-map is more suitable for this
    # return word in STOPWORDS
    _word = word.lower()
    index = bisect.bisect_left(STOPWORDS, _word)
    return STOPWORDS[index] == _word


def normalize(word):
    _word = word.translate(PUNCTUATION)
    return STEMER.stem(_word)
