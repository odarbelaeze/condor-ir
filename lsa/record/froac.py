import hashlib

from xml.dom import minidom

from .base import RecordIterator
from .base import RecordParser

from .util import gen_to_list
from .util import xml_to_text


class FroacRecordParser(RecordParser):

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

    @xml_to_text
    def _clear_language(self, raw):
        return raw.getElementsByTagName('lom:language').item(0)

    @gen_to_list
    def _clear_keywords(self, raw):
        keywords = raw.getElementsByTagName('lom:keyword')
        for keyword in keywords:
            yield keyword.firstChild.nodeValue

    def _clear_hash(self, raw):
        sha = hashlib.sha1()
        sha.update(raw.toxml().encode('utf-8'))
        return sha.hexdigest()


class FroacRecordIterator(RecordIterator):

    '''
    Iterates plain txt froac records in a file.
    '''

    parser_class = FroacRecordParser

    def get_buffer(self):
        dom = minidom.parse(self.filename)
        for dom_element in dom.getElementsByTagName('record'):
            yield dom_element
