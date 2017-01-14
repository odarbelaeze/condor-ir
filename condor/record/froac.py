import hashlib

from xml.dom import minidom

from condor.record.base import RecordIterator
from condor.record.base import RecordParser

from condor.util import gen_to_list
from condor.util import xml_to_text


class FroacRecordParser(RecordParser):

    language_key = {
        'es': 'spanish',
        'en': 'english',
        'pt': 'portuguese',
        'fr': 'french',
        'it': 'italian',
        'de': 'german',
    }

    default_language = 'english'

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

    def _clear_language(self, raw):
        langNode = raw.getElementsByTagName('lom:language').item(0)
        if langNode is None:
            return self.default_language
        lang = langNode.firstChild.nodeValue
        return self.language_key.get(lang, self.default_language)

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
