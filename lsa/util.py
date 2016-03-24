'''
Contains utility functions to work with tokens and decorators
to work with XML, lists and generators.
'''
import bisect
import collections
import functools
import string

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


STOPWORDS = sorted(stopwords.words())

STEMER = SnowballStemmer('spanish')

PUNCTUATION = str.maketrans(dict.fromkeys(string.punctuation))


def xml_to_text(func):
    '''
    Transforms a function that would return an XML element into a function
    that returns the text content of the XML element as a string.
    '''
    @functools.wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            return ''
        return result.firstChild.nodeValue
    return inner


def gen_to_list(func):
    '''
    Transforms a function that would return a generator into a function that
    returns a list of the generated values, ergo, do not use this decorator
    with infinite generators.
    '''
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return list(func(*args, **kwargs))
    return inner


def isi_text_to_dic(text):
    '''
    This function takes in any ISI WOS plain text formatted string and turns it
    into a dictionary where the keys are the two letter leading keys and the
    values are a list of the strings under that key.
    '''
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
    '''
    Checks if a word is a stopword using the bisection method over a list of
    known stopwords stored in a global variable.
    '''
    # TODO A hash-map is more suitable for this
    # return word in STOPWORDS
    _word = word.lower()
    index = bisect.bisect_left(STOPWORDS, _word)
    return STOPWORDS[index] == _word


def normalize(word):
    '''
    Filters out the punctuation from a word and then applies a steemer, and
    yields the steemed word.
    '''
    # TODO This obviously may take a word normalizer class, to control the
    #      language and other normalization parameters
    _word = word.translate(PUNCTUATION)
    return STEMER.stem(_word)


def to_list(obj):
    '''
    Transforms a non iterable object into a singleton list, or an iterable
    into a list.
    '''
    if isinstance(obj, list) or isinstance(obj, tuple):
        return list(obj)
    return [obj]
