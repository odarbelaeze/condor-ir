'''
This module contains utilities to normalize words and simplify them, it should
be able to remove punctuation, filter out stopwords and maybe transform some
latex accents into unicode accent characters.
'''

import bisect
import string

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


STOPWORDS = sorted(stopwords.words())

STEMER = SnowballStemmer('spanish')

PUNCTUATION = str.maketrans(dict.fromkeys(string.punctuation))


class SpaceTokenizer(object):

    '''
    Simple tokenization based on spaces
    '''

    def tokenize(self, sentence):
        return sentence.split()


class Normalizer(object):

    default_tokenizer = SpaceTokenizer
    default_language = 'spanish'

    def __init__(self, language=None, tokenizer=None):
        self.language = language or self.default_language
        self.tokenizer = tokenizer or self.default_tokenizer()

    def apply_to(self, sentence):
        return sentence


class PunctuationRemover(Normalizer):

    '''
    Removes punctuation from a sentence
    '''

    characters = string.punctuation

    def __init__(self, characters=None, **kwargs):
        self.translation = str.maketrans(
            dict.fromkeys(characters or self.characters)
        )
        super().__init__(**kwargs)

    def apply_to(self, sentence):
        return super().apply_to(sentence.translate(self.translation))


class Stemmer(Normalizer):

    '''
    Changes words to their respective stemms
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stemmer = SnowballStemmer(self.language)

    def apply_to(self, sentence):
        tokens = self.tokenizer.tokenize(sentence)
        result = ' '.join(self.stemmer.stem(token) for token in tokens)
        return super().apply_to(result)


class StopwordRemover(Normalizer):

    '''
    Removes stopwords from a sentence
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stopwords = {
            word: None for word in stopwords.words(fileids=self.language)
        }

    def apply_to(self, sentence):
        tokens = self.tokenizer.tokenize(sentence)
        result = ' '.join(
            token for token in tokens if token not in self.stopwords
        )
        return super().apply_to(result)


def is_stopword(word):
    '''
    Checks if a word is a stopword using the bisection method over a list of
    known stopwords stored in a global variable.
    '''
    # TODO A hash-map is more suitable for this
    # return word in STOPWORDS
    _word = word.lower()
    index = bisect.bisect_left(STOPWORDS, _word)
    return STOPWORDS[index] == _word


def normalize(word):
    '''
    Filters out the punctuation from a word and then applies a steemer, and
    yields the steemed word.
    '''
    # TODO This obviously may take a word normalizer class, to control the
    #      language and other normalization parameters
    _word = word.translate(PUNCTUATION)
    return STEMER.stem(_word)
