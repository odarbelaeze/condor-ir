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
from condor.record import record_iterator_class


class Bibliography(AuditableMixing, DeclarativeBase):

    __tablename__ = 'bibliography'

    bibliography_set_eid = Column(
        Unicode(40),
        ForeignKey('bibliography_set.eid')
    )

    hash = Column(Unicode(40), nullable=False)
    title = Column(Unicode(512), nullable=False)
    description = Column(Unicode, nullable=False)
    keywords = Column(Unicode, nullable=False)
    language = Column(Unicode(16), nullable=False)
    full_text_path = Column(Unicode(512), nullable=True)

    bibliography_set = relationship(
        'BibliographySet',
        back_populates='bibliographies',
    )

    def raw_data(self, fields, normalizer_class):
        """
        Get the raw data from the given fields in this record.

        :param fields: fields of interest
        :param normalizer_class: normalizer for the data
        :return: list of normalized data
        """
        normalizer = normalizer_class(language=self.language)
        data = ' '.join(getattr(self, field) for field in fields)
        return normalizer.apply_to(data).split()

    @property
    def full_text(self):
        """
        Retrieve full text.
        :return: string with the full text
        """
        if not self.full_text_path:
            return ''
        return ' '.join(open(self.full_text_path).read().split('\n'))

    @staticmethod
    def mappings_from_files(file_names, record_type, **kwargs):
        """
        Creates bibliography mappings out of files.

        :param file_names: paths to the files
        :param record_type: type of record to extract
        :param kwargs: extra fields to include in the mappings
        :return: an iterable over mappings
        """
        iterator_class = record_iterator_class(record_type)
        records = dict()
        for file in file_names:
            for record in iterator_class(file):
                record['keywords'] = '; '.join(record.get('keywords', ''))
                record.update(kwargs)
                records[record['hash']] = record

        return [record for record in records.values()]
