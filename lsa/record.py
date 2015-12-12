from .util import gen_to_list
from .util import is_stopword
from .util import isi_text_to_dic
from .util import xml_to_text


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


class IsiRecord(Record):
    """This represents an ISI web of knowledge record"""

    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text                    # It is a plain text record anyway
        dic = isi_text_to_dic(text)
        self.title = ' '.join(dic.get('TI', ['']))
        self.description = ' '.join(dic.get('AB', ['']))
        self.keywords = dic.get('ID', []) + dic.get('DE', [])
