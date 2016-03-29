import pytest

from lsa.normalize import PunctuationRemover
from lsa.normalize import Stemmer
from lsa.normalize import StopwordRemover
from lsa.normalize import Lowercaser


@pytest.fixture(scope="module")
def punctuated():
    return 'hola, que hace?'


@pytest.fixture(scope="module")
def punctuation():
    return PunctuationRemover()


@pytest.fixture(scope="module")
def stemmer():
    return Stemmer()


@pytest.fixture(scope="module")
def stopwords():
    return StopwordRemover()


@pytest.fixture(scope="module")
def lowercase():
    return Lowercaser()


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


def test_stopword_remover_removes_stopwords(stopwords):
    result = stopwords.apply_to('costa de concordia')
    assert 'de' not in result


def test_stopword_remover_keeps_important_words(stopwords):
    result = stopwords.apply_to('costa de concordia')
    assert 'costa concordia' == result


def test_normalizers_can_be_composed(punctuated):
    class Composed(PunctuationRemover, StopwordRemover, Stemmer):
        pass
    print(Composed.__mro__)
    normalizer = Composed()
    result = normalizer.apply_to(punctuated)
    assert 'hol hac' == result


def test_lowercase_normalizer_lowercases_tokens(lowercase):
    result = lowercase.apply_to('Title Cased Phrase')
    assert result.islower()


def test_lowercase_normalizer_keeps_all_tokens(lowercase):
    result = lowercase.apply_to('Title Cased Phrase')
    assert 'title cased phrase' == result
