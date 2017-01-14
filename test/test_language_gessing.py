import pytest

from condor.util import LanguageGuesser


@pytest.fixture(scope='module')
def guesser(request):
    return LanguageGuesser()


def test_language_guesser_can_be_instantiated(guesser):
    assert guesser is not None


def test_language_guesser_counts_right(guesser):
    es_counts = guesser.counts('hola, ¿qué hace?')
    assert 3 == es_counts['es_CO']
    assert 0 == es_counts['en_US']
    assert 0 == es_counts['fr_FR']


def test_language_guesser_guesess_languages_for_different_sentences(guesser):
    assert 'spanish' == guesser.guess('hola, ¿qué hace?')
    assert 'english' == guesser.guess('hello, how are you?')
    assert 'french' == guesser.guess('je suis un homme')
    assert 'german' == guesser.guess('ich trinke das Wasser')


def test_language_guesser_falls_back_to_default_lang(guesser):
    assert 'english' == guesser.guess(
        'askdfjlask klajsd flkajslk ajlsdkfj alskdf'
    )


def test_language_guesser_checks_dominant_language(guesser):
    assert 'english' == guesser.guess('hello how are you man hola que hace')
    assert 'spanish' == guesser.guess('hello how are hola que hay de nuevo')


def test_language_guesser_preferences(guesser):
    assert 'english' == guesser.guess(
        'Communications in Computer and Information Science'
    )
