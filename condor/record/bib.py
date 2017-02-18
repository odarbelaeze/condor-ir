import bibtexparser
import hashlib
import re

from condor.record.base import RecordIterator
from condor.record.base import RecordParser
from condor.util import LanguageGuesser

from condor.normalize import LatexAccentRemover


class BibtexRecordParser(RecordParser):

    mappings = {
        'description': 'abstract',
    }

    guesser = LanguageGuesser()

    accent_remover = LatexAccentRemover()

    def _clear_keywords(self, raw):
        line = raw.get('keyword', '')
        return re.split(r'[,; ]+', line)

    def _clear_hash(self, raw):
        sha = hashlib.sha1()
        data = self.clear('title', raw) + self.clear('description', raw)
        sha.update(data.encode('utf-8'))
        return sha.hexdigest()

    def _clear_language(self, raw):
        data = self.clear('title', raw) + self.clear('description', raw)
        data += ' '.join(self.clear('keywords', raw))
        return raw.get('language', self.guesser.guess(data)).lower()

    def clear(self, field, raw):
        mapping = self.get_mapping(field)
        cleared = raw.get(mapping, super().clear(field, raw))
        if field in self.list_fields:
            return [self.accent_remover.apply_to(item) for item in cleared]
        return self.accent_remover.apply_to(cleared)

    def parse(self, raw):
        if isinstance(raw, str):
            return super().parse(bibtexparser.loads(raw).entries[0])
        return super().parse(raw)


class BibtexRecordIterator(RecordIterator):

    '''
    Iterates over bibtex reccords
    '''

    parser_class = BibtexRecordParser

    def get_buffer(self):
        with open(self.filename, 'r') as bibtex:
            database = bibtexparser.load(bibtex)
            for entry in database.entries:
                yield entry
