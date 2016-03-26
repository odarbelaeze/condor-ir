import functools
import hashlib
import operator
import re

import bibtexparser

from xml.dom import minidom

from .util import gen_to_list
from .util import isi_text_to_dic
from .util import xml_to_text
from .util import to_list


class RecordParser(object):

    '''
    Outlines the API for parsing different kinds of records into dictionaries
    that are easy to use and store.
    '''

    mappings = {}

    def __init__(self, interest_fields=None, list_fields=None):
        '''
        Initializes a record parser with a couple of `interest_fields` and
        a verbose list of `list_fields` the list fields are a hint for the
        parser to return list of string instead of a string for the given
        keys.
        '''
        self.interest_fields = interest_fields or [
            'uuid', 'title', 'keywords', 'description',
        ]
        self.list_fields = list_fields or ['keywords']

    def get_default(self, field):
        '''
        Returns the default value for a given `field`
        '''
        if field in self.list_fields:
            return []
        return ''

    def clear(self, field, raw):
        '''
        Clears the given `field` out of a raw data record.
        '''
        if hasattr(self, '_clear_' + field):
            return getattr(self, '_clear_' + field)(raw)
        return None

    def parse(self, raw):
        '''
        Returns a dictionary of the interest fields in the metadata.
        '''
        data = {
            field: self.clear(field, raw)
            for field in self.interest_fields
        }
        return data


class FroacRecordParser(RecordParser):

    def clear(self, field, raw):
        if field in ['title', 'keywords', 'uuid', 'description']:
            return getattr(self, '_clear_' + field)(raw)
        raise NotImplementedError(
            'The field ' + field + 'has not been implemented')

    def parse(self, raw):
        if isinstance(raw, str):
            return super().parse(minidom.parseString(raw))
        return super().parse(raw)

    @xml_to_text
    def _clear_title(self, raw):
        return raw.getElementsByTagName('lom:title').item(0)

    @xml_to_text
    def _clear_description(self, raw):
        return raw.getElementsByTagName('lom:description').item(0)

    @gen_to_list
    def _clear_keywords(self, raw):
        keywords = raw.getElementsByTagName('lom:keyword')
        for keyword in keywords:
            yield keyword.firstChild.nodeValue

    def _clear_uuid(self, raw):
        sha = hashlib.sha1()
        sha.update(raw.toxml().encode('utf-8'))
        return sha.hexdigest()


class IsiRecordParser(RecordParser):

    """This represents an ISI web of knowledge record"""

    def __init__(self, keys=None, **kwargs):
        super().__init__(**kwargs)
        self._keys = keys or {
            'title': 'TI',
            'description': 'AB',
            'keywords': ['ID', 'DE'],
            'uuid': 'UT'
        }

    def parse(self, raw):
        if isinstance(raw, str):
            return super().parse(isi_text_to_dic(raw))
        return super().parse(raw)

    def _is_list(self, field):
        return field in ['keywords']

    def _get_list_from_key(self, field, raw):
        keys = to_list(self._keys.get(field))
        return functools.reduce(operator.add, [raw.get(k, []) for k in keys])

    def _get_from_key(self, field, raw):
        return ' '.join(self._get_list_from_key(field, raw))

    def clear(self, field, raw):
        if self._is_list(field):
            return self._get_list_from_key(field, raw)
        return self._get_from_key(field, raw)


class BibtexRecordParser(RecordParser):

    mappings = {
        'keywords': 'keyword'
    }

    def _clear_keywords(self, raw):
        line = raw.get(self.get_mapping('keywords'), '')
        return re.split(r'[,; ]+', line)

    def _clear_uuid(self, raw):
        sha = hashlib.sha1()
        data = self.clear('title', raw) + self.clear('description', raw)
        sha.update(data.encode('utf-8'))
        return sha.hexdigest()

    def get_mapping(self, field):
        return self.mappings.get(field, field)

    def clear(self, field, raw):
        data = super().clear(field, raw)
        if data is not None:
            return data
        _field = self.get_mapping(field)
        default = super().get_default(field)
        return raw.get(_field, default)

    def parse(self, raw):
        if isinstance(raw, str):
            return super().parse(bibtexparser.loads(raw).entries[0])
        return super().parse(raw)


class RecordIterator(object):

    '''
    Iterates over a bunch of reccords in a file.
    '''

    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        '''
        Not implemented by default. Iterates over all the records in
        the file given by the filename.
        '''
        raise NotImplementedError('Use a specialized implementation')


class FroacRecordIterator(RecordIterator):

    '''
    Iterates plain txt froac records in a file.
    '''

    def __iter__(self):
        dom = minidom.parse(self.filename)
        parser = FroacRecordParser()
        for dom_element in dom.getElementsByTagName('record'):
            yield parser.parse(dom_element)


class IsiRecordIterator(RecordIterator):

    '''
    Iterates over a file with ISI txt reccords while yielding reccords.
    '''

    def __iter__(self):
        buff = []
        parser = IsiRecordParser()
        for line in open(self.filename):
            buff.append(line)
            if line[:2] == 'ER':
                yield parser.parse('\n'.join(buff))
                buff = []


class BibtexRecordIterator(RecordIterator):

    '''
    Iterates over bibtex reccords
    '''

    parser_class = BibtexRecordParser

    def __iter__(self):
        with open(self.filename, 'r') as bibtex:
            database = bibtexparser.load(bibtex)
            parser = self.parser_class()
            for entry in database.entries:
                yield parser.parse(entry)
