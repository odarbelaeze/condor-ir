import hashlib
import uuid

from xml.dom import minidom

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

    @property
    def metadata(self):
        return {
            'uuid': self.uuid,
            'title': self.title,
            'keywords': self.keywords,
            'description': self.description,
            'tokens': list(self.tokens()),
            'raw': self.raw,
        }


class FroacRecord(Record):

    def __init__(self, raw, **kwargs):
        super().__init__(**kwargs)
        self._raw = raw

    @property
    @xml_to_text
    def title(self):
        return self._raw.getElementsByTagName('lom:title').item(0)

    @property
    @xml_to_text
    def description(self):
        return self._raw.getElementsByTagName('lom:description').item(0)

    @property
    @gen_to_list
    def keywords(self):
        keywords = self._raw.getElementsByTagName('lom:keyword')
        for keyword in keywords:
            yield keyword.firstChild.nodeValue

    @property
    def raw(self):
        return self._raw.toxml()

    @property
    def uuid(self):
        sha = hashlib.sha1()
        sha.update(self.raw.encode('utf-8'))
        return sha.hexdigest()


class FroacRecordSet(object):

    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        dom = minidom.parse(self.filename)
        for dom_element in dom.getElementsByTagName('record'):
            yield FroacRecord(dom_element)

    def metadata(self):
        for record in self:
            yield record.metadata


class IsiRecord(Record):
    """This represents an ISI web of knowledge record"""

    def __init__(self, raw, **kwargs):
        super().__init__(**kwargs)
        self.raw = raw
        dic = isi_text_to_dic(raw)
        self.title = ' '.join(dic.get('TI', ['']))
        self.description = ' '.join(dic.get('AB', ['']))
        self.keywords = dic.get('ID', []) + dic.get('DE', [])
        self.uuid = dic.get('UT', ['{}'.format(uuid.uuid4())])[0]


class IsiRecordSet(object):

    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        buff = []
        for line in open(self.filename):
            buff.append(line)
            if line[:2] == 'ER':
                yield IsiRecord('\n'.join(buff))
                buff = []

    def metadata(self):
        for record in self:
            yield record.metadata
