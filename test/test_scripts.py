import pytest

from click.testing import CliRunner

from condor.scripts.model import condormodel
from condor.scripts.populate import condorpopulate
from condor.scripts.query import condorquery


@pytest.fixture
def runner():
    return CliRunner()


def test_basic_usage(runner):
    res = runner.invoke(condorpopulate, [])
    assert res.exit_code == 2
    assert 'Usage' in res.output


def test_populate_bibtex(runner):
    res = runner.invoke(
        condorpopulate,
        ['--bib', '--verbose', 'data/bib/*.bib']
    )
    assert res.exit_code == 0
    assert 'The database contains 3 records' in res.output


def test_basic_usage_model(runner):
    res = runner.invoke(condormodel, ['--help'])
    assert res.exit_code == 0
    assert 'Usage' in res.output


def test_basic_usagle_query(runner):
    res = runner.invoke(condorquery, [])
    assert res.exit_code == 2
    assert 'Usage' in res.output
