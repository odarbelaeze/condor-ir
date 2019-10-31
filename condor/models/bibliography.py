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
from condor.models.document import Document


class Bibliography(AuditableMixing, DeclarativeBase):
    """
    Describes a group of documents.
    """

    __tablename__ = 'bibliography'

    description = Column(Unicode(4096), nullable=False)

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

    @classmethod
    def from_files(cls, kind, files,
                   full_text=None, no_cache=False,
                   description=None, languages=None,
                   show_progress_bar=False):
        """
        Creates a bibliography and attached documents.

        :param str kind: bib, froac, xml, or isi the kind of file to work with
        :param list files: list of File objects to read from
        :param str full_text: try to find the full text in this directory
        :param bool no_cache: ignore cache when reading full text
        :param str description: description of the bibliography
        :param list languages: filter to documents of these languages only
        """
        count = len(files)
        description = description or f'Document set from {count} {kind} files.'
        bibliography = Bibliography(description=description)
        mappings = Document.mappings_from_files(
            kind,
            files,
            full_text_path=full_text,
            force=no_cache,
            show_progress_bar=show_progress_bar,
        )
        if languages:
            languages_text = ', '.join(languages)
            bibliography.description += f' Filtered to {languages_text}'
            mappings = [
                m
                for m in mappings
                if m.get('language', 'english').lower() in languages
            ]
        bibliography.documents = [Document(**mapping) for mapping in mappings]
        return bibliography
