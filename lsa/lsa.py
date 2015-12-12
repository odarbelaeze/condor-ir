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


def is_stopword(word):
    # TODO A hsh-map is more suitable for this
    # return word in STOPWORDS
    _word = word.lower()
    index = bisect.bisect_left(STOPWORDS, _word)
    return STOPWORDS[index] == _word


def normalize(word):
    _word = word.translate(PUNCTUATION)
    return STEMER.stem(_word)


class Record(object):

    def __init__(self, strip_stopwords=False):
        self.strip_stopwords = strip_stopwords

    @property
    @gen_to_list
    def raw(self):
        tokens = [self.title, self.description, ] + self.keywords
        tokens = ' '.join(tokens).split(' ')
        valid = filter(lambda x: not (x == '' or x.isspace()), tokens)
        if self.strip_stopwords:
            return filter(lambda x: not is_stopword(x), valid)
        return valid


class FroacRecord(Record):

    def __init__(self, xml, **kwargs):
        super().__init__(**kwargs)
        self.xml = xml

    @property
    @xml_to_text
    def title(self):
        return self.xml.getElementsByTagName('lom:title').item(0)

    @property
    @xml_to_text
    def description(self):
        return self.xml.getElementsByTagName('lom:description').item(0)

    @property
    @gen_to_list
    def keywords(self):
        keywords = self.xml.getElementsByTagName('lom:keyword')
        for keyword in keywords:
            yield keyword.firstChild.nodeValue


class FroacRecordSet(object):

    def __init__(self, xml):
        self.xml = xml

    def __iter__(self):
        for node in self.xml.getElementsByTagName('record'):
            yield FroacRecord(node)


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


class IsiRecord(Record):
    """This represents an ISI web of knowledge record"""

    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text                    # It is a plain text record anyway
        dic = isi_text_to_dic(text)
        self.title = ' '.join(dic.get('TI', ['']))
        self.description = ' '.join(dic.get('AB', ['']))
        self.keywords = dic.get('ID', []) + dic.get('DE', [])
