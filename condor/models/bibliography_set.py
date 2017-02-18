from sqlalchemy import (
    Column,
    Unicode,
)

from sqlalchemy.orm import relationship

from condor.models.base import AuditableMixing, DeclarativeBase
from condor.record import record_iterator_class


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

    @classmethod
    def from_file_list(cls, file_names, record_type, **kwargs):
        """
        Create a bibliography set from a list of files and a record kind
        
        :param file_names: the list of file names to use
        :param record_type: the record type of the files
        :return: a tuple of the bibliography set and bibliographies
        """
        iterator_class = record_iterator_class(record_type)
        records = dict()
        for file in file_names:
            for record in iterator_class(file):
                record['keywords'] = '; '.join(record.get('keywords', ''))
                records[record['hash']] = record
        return cls(**kwargs), records.values()
