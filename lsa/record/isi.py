from .base import RecordParser
from .base import RecordIterator

from .util import isi_text_to_dic


class IsiRecordParser(RecordParser):

    """This represents an ISI web of knowledge record"""

    mappings = {
        'title': 'TI',
        'description': 'AB',
        'keywords': 'ID',
        'uuid': 'UT',
    }

    def parse(self, raw):
        if isinstance(raw, str):
            return super().parse(isi_text_to_dic(raw))
        return super().parse(raw)

    def clear(self, field, raw):
        _field = self.get_mapping(field)
        if field in self.list_fields:
            return raw.get(_field, super().clear(field, raw))
        try:
            return ' '.join(raw.get(_field))
        except KeyError:
            return self.get_default(field)


class IsiRecordIterator(RecordIterator):

    '''
    Iterates over a file with ISI txt reccords while yielding reccords.
    '''

    parser_class = IsiRecordParser

    def get_buffer(self):
        buff = []
        for line in open(self.filename):
            buff.append(line)
            if line[:2] == 'ER':
                yield '\n'.join(buff)
                buff = []
