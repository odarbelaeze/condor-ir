from lsa.lsa import STOPWORDS
from lsa.lsa import is_stopword
from lsa.metadata import is_valid
import random


def test_is_stopword_works_with_upper_case_words():
    word = random.choice(STOPWORDS)
    assert is_stopword(word.upper())


def test_is_stopword_works_with_lower_case_words():
    word = random.choice(STOPWORDS)
    assert is_stopword(word.lower())


def test_is_valid_yields_good_values():
    words = {
        '123123': True,
        'askdfj': True,
        ' ': False,
        '123asdf': True,
        '\t': False,
    }
    for word, valid in words.items():
        assert valid == is_valid(word)
