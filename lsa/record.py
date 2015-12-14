from .util import gen_to_list
from .util import is_stopword
from .util import isi_text_to_dic
from .util import xml_to_text


class Record(object):

    def __init__(self, strip_stopwords=False):
        self.strip_stopwords = strip_stopwords

    @gen_to_list
    def tokens(self):
        tokens = [self.title, self.description, ] + self.keywords
        tokens = ' '.join(tokens).split(' ')
        valid = filter(lambda x: not (x == '' or x.isspace()), tokens)
        if self.strip_stopwords:
            return filter(lambda x: not is_stopword(x), valid)
        return valid


class FroacRecord(Record):

    def __init__(self, raw, **kwargs):
        super().__init__(**kwargs)
        self.raw = raw

    @property
    @xml_to_text
    def title(self):
        return self.raw.getElementsByTagName('lom:title').item(0)

    @property
    @xml_to_text
    def description(self):
        return self.raw.getElementsByTagName('lom:description').item(0)

    @property
    @gen_to_list
    def keywords(self):
        keywords = self.raw.getElementsByTagName('lom:keyword')
        for keyword in keywords:
            yield keyword.firstChild.nodeValue


class FroacRecordSet(object):

    def __init__(self, raw):
        self.raw = raw

    def __iter__(self):
        for node in self.raw.getElementsByTagName('record'):
            yield FroacRecord(node)


class IsiRecord(Record):
    """This represents an ISI web of knowledge record"""

    def __init__(self, raw, **kwargs):
        super().__init__(**kwargs)
        self.raw = raw
        dic = isi_text_to_dic(raw)
        self.title = ' '.join(dic.get('TI', ['']))
        self.description = ' '.join(dic.get('AB', ['']))
        self.keywords = dic.get('ID', []) + dic.get('DE', [])
