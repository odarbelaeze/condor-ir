'''
This module describes the API for a record parser and a record iterator, they
have the responsibility of transforming a chunk of text into a usable
dictionary and go through a file and find all the records.
'''


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
            parsed = parser.parse(item)
            important_fields = dict(parsed, language=None, hash=None)
            # Omit all the null records, no title, abstract or keywords
            if all(not i for i in important_fields.values()):
                continue
            yield parsed
