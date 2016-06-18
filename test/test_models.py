import pytest

from condor.dbutil import session as Session
from condor.models import (
    Bibliography,
    BibliographySet,
    TermDocumentMatrix,
    RankingMatrix,
)


@pytest.yield_fixture(scope='function')
def session():
    _session = Session()
    yield _session
    _session.rollback()
    _session.close()


@pytest.fixture
def bibset(session):
    bibset = BibliographySet(description='asdkfjaskldf')
    session.add(bibset)
    session.flush()
    return bibset


def test_bibliographies_are_deleted(session, bibset):
    bibliography = Bibliography(bibliography_set_eid=bibset.eid)
    session.flush()
    bib_eid = bibliography.eid
    session.delete(bibset)
    session.flush()
    assert session.query(Bibliography).filter(
        Bibliography.eid == bib_eid
    ).first() is None


def test_matrices_and_engines_are_deleted(session, bibset):
    term_matrix = TermDocumentMatrix(
        bibliography_set_eid=bibset.eid,
        bibliography_options='',
        processing_options='',
        term_list_path='',
        tdidf_matrix_path='',
    )
    session.add(term_matrix)
    session.flush()
    term_eid = term_matrix.eid
    rank_matrix = RankingMatrix(
        term_document_matrix_eid=term_eid,
        kind='',
        build_options='',
        ranking_matrix_path='',
    )
    session.add(rank_matrix)
    session.flush()
    rank_eid = rank_matrix.eid
    assert term_eid is not None
    assert rank_eid is not None
    session.delete(bibset)
    session.flush()
    assert session.query(TermDocumentMatrix).filter(
        TermDocumentMatrix.eid == term_eid
    ).first() is None
    assert session.query(RankingMatrix).filter(
        RankingMatrix.eid == rank_eid
    ).first() is None


def test_engines_are_deleted(session, bibset):
    term_matrix = TermDocumentMatrix(
        bibliography_set_eid=bibset.eid,
        bibliography_options='',
        processing_options='',
        term_list_path='',
        tdidf_matrix_path='',
    )
    session.add(term_matrix)
    session.flush()
    term_eid = term_matrix.eid
    rank_matrix = RankingMatrix(
        term_document_matrix_eid=term_eid,
        kind='',
        build_options='',
        ranking_matrix_path='',
    )
    session.add(rank_matrix)
    session.flush()
    rank_eid = rank_matrix.eid
    assert term_eid is not None
    assert rank_eid is not None
    session.delete(bibset)
    session.flush()
    assert session.query(TermDocumentMatrix).filter(
        TermDocumentMatrix.eid == term_eid
    ).first() is None
    assert session.query(RankingMatrix).filter(
        RankingMatrix.eid == rank_eid
    ).first() is None
