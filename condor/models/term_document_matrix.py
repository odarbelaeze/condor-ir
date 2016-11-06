import numpy

from sqlalchemy import (
    Column,
    ForeignKey,
    Unicode,
)

from sqlalchemy.orm import relationship

from condor.models.base import (
    AuditableMixing,
    DeclarativeBase,
)


class TermDocumentMatrix(AuditableMixing, DeclarativeBase):

    __tablename__ = 'term_document_matrix'

    bibliography_set_eid = Column(
        Unicode(40),
        ForeignKey('bibliography_set.eid')
    )

    bibliography_options = Column(Unicode(512), nullable=False)
    processing_options = Column(Unicode(512), nullable=False)
    term_list_path = Column(Unicode(512), nullable=False)
    tdidf_matrix_path = Column(Unicode(512), nullable=False)

    bibliography_set = relationship(
        'BibliographySet',
        back_populates='term_document_matrices',
    )

    ranking_matrices = relationship(
        'RankingMatrix',
        back_populates='term_document_matrix',
        cascade='all, delete-orphan',
    )

    @property
    def terms(self):
        with open(self.term_list_path) as term_file:
            terms = term_file.read().split('\n')
        return terms

    @property
    def matrix(self):
        return numpy.load(self.tdidf_matrix_path)
