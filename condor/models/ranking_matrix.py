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


class RankingMatrix(AuditableMixing, DeclarativeBase):

    __tablename__ = 'ranking_matrix'

    term_document_matrix_eid = Column(
        Unicode(40),
        ForeignKey('term_document_matrix.eid')
    )

    kind = Column(Unicode(16), nullable=False)
    build_options = Column(Unicode(512), nullable=False)
    ranking_matrix_path = Column(Unicode(512), nullable=False)

    term_document_matrix = relationship(
        'TermDocumentMatrix',
        back_populates='ranking_matrices',
    )
