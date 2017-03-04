from sqlalchemy import (
    Column,
    Unicode,
)

from sqlalchemy.orm import relationship

from condor.models.base import AuditableMixing, DeclarativeBase


class BibliographySet(AuditableMixing, DeclarativeBase):

    __tablename__ = 'bibliography_set'

    description = Column(Unicode, nullable=False)

    bibliographies = relationship(
        'Bibliography',
        back_populates='bibliography_set',
        cascade='all, delete-orphan',
    )

    term_document_matrices = relationship(
        'TermDocumentMatrix',
        back_populates='bibliography_set',
        cascade='all, delete-orphan',
    )

    queries = relationship(
        'Query',
        back_populates='bibliography_set'
    )
