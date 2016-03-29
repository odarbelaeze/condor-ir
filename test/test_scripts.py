import pytest

from click.testing import CliRunner

from lsa.scripts.model import lsamodel
from lsa.scripts.populate import lsapopulate
from lsa.scripts.query import lsaquery


@pytest.fixture
def runner():
    return CliRunner()


def test_basic_usage(runner):
    res = runner.invoke(lsapopulate, [])
    assert res.exit_code == 2
    assert 'Usage' in res.output


def test_populate_bibtex(runner):
    res = runner.invoke(
        lsapopulate,
        ['--bib', '--verbose', 'data/bib/*.bib']
    )
    assert res.exit_code == 0
    assert 'The database contains 3 records' in res.output


def test_basic_usage_model(runner):
    res = runner.invoke(lsamodel, ['--help'])
    assert res.exit_code == 0
    assert 'Usage' in res.output


def test_basic_usagle_query(runner):
    res = runner.invoke(lsaquery, [])
    assert res.exit_code == 2
    assert 'Usage' in res.output
