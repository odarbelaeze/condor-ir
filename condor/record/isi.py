from condor.record.base import RecordIterator
from condor.record.base import RecordParser

from condor.util import isi_text_to_dic


class IsiRecordParser(RecordParser):

    '''This represents an ISI web of knowledge record'''

    mappings = {
        'title': 'TI',
        'description': 'AB',
        'keywords': 'ID',
        'language': 'LA',
        'hash': 'UT',
    }

    def parse(self, raw):
        '''
        Checks if the input is a string if so it transforms it into a
        dictionary and runs the default `parse` method.
        '''
        if isinstance(raw, str):
            return super().parse(isi_text_to_dic(raw))
        return super().parse(raw)

    def clear(self, field, raw):
        '''
        Uses the `mappings` to get the entries out of the raw dictionary
        '''
        _default = self.get_default(field)
        _result = super().clear(field, raw)
        if _result != _default:
            return _result
        _field = self.get_mapping(field)
        if field in self.list_fields:
            return raw.get(_field, _default)
        if field == 'language':
            return ' '.join(raw.get(_field, [])).lower()
        return ' '.join(raw.get(_field, []))


class IsiRecordIterator(RecordIterator):

    '''
    Iterates over a file with ISI txt reccords while yielding reccords.
    '''

    parser_class = IsiRecordParser

    def get_buffer(self):
        '''
        Iterates over a file by looking for lines containing the ER mark
        of the isi plain text files.
        '''
        buff = []
        for line in open(self.filename):
            buff.append(line)
            if line[:2] == 'ER':
                yield '\n'.join(buff)
                buff = []
