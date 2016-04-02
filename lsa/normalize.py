'''
This module contains utilities to normalize words and simplify them, it should
be able to remove punctuation, filter out stopwords and maybe transform some
latex accents into unicode accent characters.
'''

import string

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


class SpaceTokenizer(object):

    '''
    Simple tokenization based on spaces
    '''

    def tokenize(self, text):
        return text.split()


class Normalizer(object):

    default_tokenizer = SpaceTokenizer
    default_language = 'spanish'

    def __init__(self, language=None, tokenizer=None):
        self.language = language or self.default_language
        self.tokenizer = tokenizer or self.default_tokenizer()

    def apply_to(self, text):
        return text


class PunctuationRemover(Normalizer):

    '''
    Removes punctuation from a text
    '''

    characters = string.punctuation + '¡¿'

    def __init__(self, characters=None, **kwargs):
        self.translation = str.maketrans(
            dict.fromkeys(characters or self.characters)
        )
        super().__init__(**kwargs)

    def apply_to(self, text):
        return super().apply_to(text.translate(self.translation))


class Stemmer(Normalizer):

    '''
    Changes words to their respective stemms
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stemmer = SnowballStemmer(self.language)

    def apply_to(self, text):
        tokens = self.tokenizer.tokenize(text)
        result = ' '.join(self.stemmer.stem(token) for token in tokens)
        return super().apply_to(result)


class StopwordRemover(Normalizer):

    '''
    Removes stopwords from a text
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stopwords = {
            word: None for word in stopwords.words(fileids=self.language)
        }

    def apply_to(self, text):
        tokens = self.tokenizer.tokenize(text)
        result = ' '.join(
            token for token in tokens if token not in self.stopwords
        )
        return super().apply_to(result)


class Lowercaser(Normalizer):

    '''
    Changes case to lowercase through the normalizer API
    '''

    def apply_to(self, text):
        return super().apply_to(text.lower())


class CompleteNormalizer(PunctuationRemover,
                         Lowercaser,
                         StopwordRemover,
                         Stemmer):

    '''
    A Normalizer that aggregates all the effects described in this module
    '''

    pass
