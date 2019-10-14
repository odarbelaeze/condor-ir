import pytest
from unittest.mock import Mock

from condor.util import LanguageGuesser


@pytest.fixture(scope='module')
def guesser(request):
    return LanguageGuesser()


def test_language_guesser_can_be_instantiated(guesser):
    assert guesser is not None


def test_language_guesser_guesess_languages_for_different_sentences(guesser):
    assert 'spanish' == guesser.guess('hola, ¿cómo estás?')
    assert 'english' == guesser.guess('hello, how are you?')
    assert 'french' == guesser.guess('je suis un homme')
    assert 'german' == guesser.guess('ich trinke das Wasser')


def test_language_guesser_falls_back_to_default_lang(guesser, monkeypatch):
    result = Mock()
    result.lang = 'es'
    result.prob = 0.1
    monkeypatch.setattr('langdetect.detect_langs', Mock(return_value=[result]))
    assert 'english' == guesser.guess(
        'hola suis prospect trinke das alontanarse'
    )


def test_language_guesser_checks_dominant_language(guesser):
    assert 'english' == guesser.guess('hello how are you man, what have you been up to hola hace')
    assert 'spanish' == guesser.guess('hello hola que hay de nuevo')


def test_language_guesser_preferences(guesser):
    assert 'english' == guesser.guess(
        'Communications in Computer and Information Science'
    )
