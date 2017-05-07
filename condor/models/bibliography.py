"""
Tools for handling a set of documents called bibliography.
"""

import itertools
from sqlalchemy import (
    Column,
    Unicode,
)

from sqlalchemy.orm import relationship

from condor.models.base import AuditableMixing, DeclarativeBase


class Bibliography(AuditableMixing, DeclarativeBase):
    """
    Describes a group of documents.
    """

    __tablename__ = 'bibliography'

    description = Column(Unicode, nullable=False)

    documents = relationship(
        'Document',
        back_populates='bibliography',
        cascade='all, delete-orphan',
    )

    term_document_matrices = relationship(
        'TermDocumentMatrix',
        back_populates='bibliography',
        cascade='all, delete-orphan',
    )

    queries = relationship(
        'Query',
        back_populates='bibliography'
    )

    def words(self, fields, normalizer_class):
        """
        List of normalized words from the given fields.

        :param fields: list of fields to check
        :param normalizer_class: normalizer to use
        :return: list of words
        """
        return sorted(set(itertools.chain.from_iterable(
            bib.raw_data(fields, normalizer_class)
            for bib in self.documents
        )))
