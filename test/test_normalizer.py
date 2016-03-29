import pytest

from lsa.normalize import PunctuationRemover
from lsa.normalize import Stemmer


@pytest.fixture(scope="module")
def punctuated():
    return 'hola, que hace?'


@pytest.fixture(scope="module")
def punctuation():
    return PunctuationRemover()


@pytest.fixture(scope="module")
def stemmer():
    return Stemmer()


def test_punctuation_remover_removes_puchtuation(punctuation, punctuated):
    # GIVEN any state
    # WHEN the punctuation remover is used in a punctuated phrase
    result = punctuation.apply_to(punctuated)
    # THEN the result has not punctuation at all
    assert ',' not in result
    assert '?' not in result


def test_punctuation_remover_keeps_words(punctuation, punctuated):
    result = punctuation.apply_to(punctuated)
    assert 'hola que hace' == result


def test_stemmer_changes_words_by_their_stemms(stemmer):
    result = stemmer.apply_to('hola que hace')
    assert 'hol que hac' in result
