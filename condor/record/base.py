'''
This module describes the API for a record parser and a record iterator, they
have the responsibility of transforming a chunk of text into a usable
dictionary and go through a file and find all the records.
'''

from enchant import request_dict
from collections import OrderedDict

from condor.normalize import PunctuationRemover
from condor.normalize import SpaceTokenizer


class RecordParser(object):

    '''
    Outlines the API for parsing different kinds of records into dictionaries
    that are easy to use and store.
    '''

    mappings = {}
    interest_fields = ['hash', 'title', 'keywords', 'description', 'language']
    list_fields = ['keywords', ]

    def get_mapping(self, field):
        '''
        Returns the name of a field with a modification useful when the field
        is easy to clear but it requires just a change of name.
        '''
        return self.mappings.get(field, field)

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
        return self.get_default(field)

    def parse(self, raw):
        '''
        Returns a dictionary of the interest fields in the metadata.
        '''
        data = {
            field: self.clear(field, raw)
            for field in self.interest_fields
        }
        return data


class RecordIterator(object):

    '''
    Iterates over a bunch of reccords in a file.
    '''

    parser_class = RecordParser

    def __init__(self, filename):
        self.filename = filename

    def get_buffer(self):
        raise NotImplementedError('Use an specialized class')

    def __iter__(self):
        '''
        Not implemented by default. Iterates over all the records in
        the file given by the filename.
        '''
        buff = self.get_buffer()
        parser = self.parser_class()
        for item in buff:
            yield parser.parse(item)


class LanguageGuesser(object):

    '''
    Guesses the language of a record if the record field is not
    defined
    '''

    languages = OrderedDict([
        ('en_US', 'english'),
        ('en_GB', 'english'),
        ('es_ES', 'spanish'),
        ('es_CO', 'spanish'),
        ('es_MX', 'spanish'),
        ('pt_BR', 'portuguese'),
        ('pt_PT', 'portuguese'),
        ('fr_FR', 'french'),
        ('fr_BE', 'french'),
        ('it_IT', 'italian'),
        ('de_DE', 'german'),
        ('de_CH', 'german'),
        ('de_AT', 'german'),
    ])

    default_lang = 'english'

    def __init__(self, languages=None):
        self.dictionaries = OrderedDict()
        for language in languages or self.languages:
            self.dictionaries[language] = request_dict(language)
        self.normalizer = PunctuationRemover()
        self.tokenizer = SpaceTokenizer()

    def counts(self, sentence):
        counts = OrderedDict()
        tokens = self.tokenizer.tokenize(
            self.normalizer.apply_to(sentence)
        )
        for lang, dictionary in self.dictionaries.items():
            counts[lang] = sum(dictionary.check(tk) for tk in tokens)
        return counts

    def guess(self, sentence):
        counts = self.counts(sentence)
        guessed_lang = None
        max_count = 0
        for lang, count in counts.items():
            if count > max_count:
                guessed_lang = lang
                max_count = count
        return self.languages.get(guessed_lang, self.default_lang)
