import pytest

from click.testing import CliRunner

from condor.scripts.bibset import create as bibcreate
from condor.scripts.model import create as modelcreate
from condor.scripts.query import query

from condor.scripts.bibset import bibset
from condor.scripts.matrix import matrix
from condor.scripts.ranking import ranking


@pytest.fixture
def runner():
    return CliRunner()


def test_basic_usage(runner):
    res = runner.invoke(bibcreate, [])
    assert res.exit_code == 2
    assert 'Usage' in res.output


def test_populate_bibtex(runner):
    res = runner.invoke(
        bibcreate,
        ['--bib', '--verbose', 'data/bib/*.bib']
    )
    assert res.exit_code == 0
    assert 'The database contains 3 records' in res.output


def test_basic_usage_model(runner):
    res = runner.invoke(modelcreate, ['--help'])
    assert res.exit_code == 0
    assert 'Usage' in res.output


def test_basic_usagle_query(runner):
    res = runner.invoke(query, [])
    assert res.exit_code == 2
    assert 'Usage' in res.output


def test_condor_bibset_group(runner):
    res = runner.invoke(bibset, [])
    assert res.exit_code == 0
    assert 'Usage' in res.output


def test_condor_matrix_group(runner):
    res = runner.invoke(matrix, [])
    assert res.exit_code == 0
    assert 'Usage' in res.output


def test_condor_ranking_group(runner):
    res = runner.invoke(ranking, [])
    assert res.exit_code == 0
    assert 'Usage' in res.output
