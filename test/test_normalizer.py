import pytest

from lsa.normalize import PunctuationRemover


@pytest.fixture(scope="module")
def punctuated():
    return 'hola, que hace?'


@pytest.fixture(scope="module")
def punctuation():
    return PunctuationRemover()


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
