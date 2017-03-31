"""
Contains utility functions to work with tokens and decorators
to work with XML, lists and generators.
"""

import collections
import functools
import re
from collections import OrderedDict

import PyPDF2
from enchant import request_dict

from condor.normalize import PunctuationRemover, CompleteNormalizer
from condor.normalize import SpaceTokenizer


def xml_to_text(func):
    """
    Transforms a function that would return an XML element into a function
    that returns the text content of the XML element as a string.
    """
    @functools.wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            return ''
        return result.firstChild.nodeValue
    return inner


def gen_to_list(func):
    """
    Transforms a function that would return a generator into a function that
    returns a list of the generated values, ergo, do not use this decorator
    with infinite generators.
    """
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return list(func(*args, **kwargs))
    return inner


def isi_text_to_dic(text):
    """
    This function takes in any ISI WOS plain text formatted string and turns it
    into a dictionary where the keys are the two letter leading keys and the
    values are a list of the strings under that key.
    """
    fields = collections.defaultdict(list)
    curr = ''
    for line in re.split(r'\n+', text):
        name = line[:2]
        value = line[3:]
        if not name.isspace():
            curr = name
        if not curr.isspace():
            fields[curr].append(value)
    return fields


def to_list(obj):
    """
    Transforms a non iterable object into a singleton list, or an iterable
    into a list.
    """
    if isinstance(obj, list) or isinstance(obj, tuple):
        return list(obj)
    return [obj]


class LanguageGuesser(object):

    """
    Guesses the language of a record if the record field is not
    defined
    """

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


def frequency(words, tokens):
    """
    Computes the frequency list of a list of tokens in a dense representation.

    :param list words: list of the words to look for
    :param list tokens: list of the tokens to count

    .. note:: this function applies a complete normalizer to the given tokens and guesses the language.
    """
    # word_dict = {word: pos for pos, word in enumerate(words)}
    language = LanguageGuesser().guess(' '.join(tokens))
    normalizer = CompleteNormalizer(language=language)
    counts = collections.Counter(
        normalizer.apply_to(token)
        for token in tokens
    )
    return [counts.get(word, 0) for word in words]


def full_text_from_pdf(filename):
    """
    Tries to extract text from pdfs.
    """
    chunks = []
    with open(filename, 'rb') as handle:
        try:
            pdf_reader = PyPDF2.PdfFileReader(handle)
            for page in pdf_reader.pages:
                try:
                    chunks.append(page.extractText())
                except PyPDF2.utils.PyPdfError:
                    pass
                except Exception:
                    # Some exceptions leak from PyPDF2
                    pass
        except PyPDF2.utils.PyPdfError:
            pass
        except Exception:
            # Some exceptions leak from PyPDF2
            pass
    return '\n'.join(chunks)
