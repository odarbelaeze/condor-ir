import pytest

from condor.normalize import PunctuationRemover
from condor.normalize import Stemmer
from condor.normalize import StopwordRemover
from condor.normalize import Lowercaser
from condor.normalize import LatexAccentRemover
from condor.normalize import CompleteNormalizer


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


@pytest.fixture(scope="module")
def latex():
    return LatexAccentRemover()


@pytest.fixture(scope="module")
def complete():
    return CompleteNormalizer()


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
    normalizer = Composed()
    result = normalizer.apply_to(punctuated)
    assert 'hol hac' == result


def test_lowercase_normalizer_lowercases_tokens(lowercase):
    result = lowercase.apply_to('Title Cased Phrase')
    assert result.islower()


def test_lowercase_normalizer_keeps_all_tokens(lowercase):
    result = lowercase.apply_to('Title Cased Phrase')
    assert 'title cased phrase' == result


def test_latex_accent_remover_removes_acents_from_vowels(latex):
    assert 'áéíóú' == latex.apply_to(r"\'a\'e\'i\'o\'u")


def test_latex_accent_remover_removes_acents_from_other_formats(latex):
    assert 'áéíóú' == latex.apply_to(r"{\'a}{\'e}{\'i}{\'o}{\'u}")
    assert 'áéíóú' == latex.apply_to(r"{\'{a}}{\'{e}}{\'{i}}{\'{o}}{\'{u}}")
    assert 'áéíóú' == latex.apply_to(r"\'{a}\'{e}\'{i}\'{o}\'{u}")


def test_latex_removes_acents_from_other_characters(latex):
    assert 'ñ' == latex.apply_to(r"\~n")


def test_latex_works_for_upercased_characters(latex):
    assert 'Ñ' == latex.apply_to(r"\~N")


def test_latex_accent_remover_works_with_some_cases(latex):
    assert 'didáctica' == latex.apply_to(r"did{\'{a}}ctica")


def test_complete_normalizer_works_with_some_cases(complete):
    assert 'didact' == complete.apply_to(r"did{\'{a}}ctica")
