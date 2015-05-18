import bisect
import functools

from nltk.corpus import stopwords


# STOPWORDS = {k: k for k in stopwords.words()}
STOPWORDS = sorted(stopwords.words())


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
    index = bisect.bisect_left(STOPWORDS, word)
    return STOPWORDS[index] == word


class Record(object):
    def __init__(self, xml, strip_stopwords=False):
        self.xml = xml
        self.strip_stopwords = strip_stopwords

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

    @property
    @gen_to_list
    def raw(self):
        tokens = [self.title, self.description, ] + self.keywords
        valid = filter(lambda x: not (x == '' or x.isspace()), tokens)
        if self.strip_stopwords:
            return filter(lambda x: not is_stopword(x), valid)
        return valid


class RecordSet(object):
    def __init__(self, xml):
        self.xml = xml

    def __iter__(self):
        for node in self.xml.getElementsByTagName('record'):
            yield Record(node)
