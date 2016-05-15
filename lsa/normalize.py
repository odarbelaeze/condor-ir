'''
This module contains utilities to normalize words and simplify them, it should
be able to remove punctuation, filter out stopwords and maybe transform some
latex accents into unicode accent characters.
'''

import re
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
        if language is not None:
            self.language = language.lower()
        else:
            self.language = self.default_language
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


class LatexAccentRemover(Normalizer):

    '''
    Removes latex accents like `\\'{a}` and makes them unicode chars `á`.
    '''

    accents = {
        '\'': {
            'a': 'á',
            'e': 'é',
            'i': 'í',
            'o': 'ó',
            'u': 'ú',
        },
        '`': {
            'a': 'à',
            'e': 'è',
            'i': 'ì',
            'o': 'ò',
            'u': 'ù',
        },
        '~': {
            'n': 'ñ',
            'o': 'õ',
            'a': 'ã',
        },
        '^': {
            'a': 'â',
            'e': 'ê',
            'i': 'î',
            'o': 'ô',
            'u': 'û',
        },
        '"': {
            'a': 'ä',
            'e': 'ë',
            'i': 'ï',
            'o': 'ö',
            'u': 'ü',
            'y': 'ÿ',
        },
        'a': {
            'e': 'æ',
        },
        'c': {
            'c': 'ç',
        },
        'o': {
            'e': 'œ',
        },
        's': {
            's': 'ß',
        },
        'v': {
            's': 'š',
        },
    }

    formats = [
        r"{{\{accent}{{{character}}}}}",
        r"{{\{accent}{character}}}",
        r"\{accent}{{{character}}}",
        r"\{accent}{character}",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _replacements(self):
        for accent, cases in self.accents.items():
            for character, modification in cases.items():
                for format_ in self.formats:
                    latex = format_.format(accent=accent, character=character)
                    yield (
                        latex,
                        modification,
                    )
                    yield (
                        latex.upper(),
                        modification.upper(),
                    )

    def apply_to(self, text):
        result = text
        for old, new in self._replacements():
            result = result.replace(old, new)
        return super().apply_to(result)


class CompleteNormalizer(LatexAccentRemover,
                         PunctuationRemover,
                         Lowercaser,
                         StopwordRemover,
                         Stemmer):

    '''
    A Normalizer that aggregates all the effects described in this module
    '''

    pass
