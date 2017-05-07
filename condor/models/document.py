"""
A tool for managing single documents within a bibliography.
"""

import os
import glob

from sqlalchemy import Column, ForeignKey, Unicode
from sqlalchemy.orm import relationship
from tqdm import tqdm

from condor.config import FULL_TEXT_PATH
from condor.models.base import AuditableMixing, DeclarativeBase
from condor.normalize import LatexAccentRemover
from condor.record import record_iterator_class
from condor.util import full_text_from_pdf


class Document(AuditableMixing, DeclarativeBase):
    """
    Describes a single document.
    """

    __tablename__ = 'document'

    bibliography_eid = Column(
        Unicode(40),
        ForeignKey('bibliography.eid')
    )

    hash = Column(Unicode(40), nullable=False)
    title = Column(Unicode(512), nullable=False)
    description = Column(Unicode, nullable=False)
    keywords = Column(Unicode, nullable=False)
    language = Column(Unicode(16), nullable=False)
    full_text_path = Column(Unicode(512), nullable=True)

    bibliography = relationship(
        'Bibliography',
        back_populates='documents',
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
    def load_full_text(record, files, force=False):
        accent_remover = LatexAccentRemover()
        filename = accent_remover.apply_to(record.get('file'))
        if not filename:
            return
        basename = os.path.basename(
            ':'.join(filename.split(':')[:-1])
        )
        full_text_path = os.path.join(
            FULL_TEXT_PATH,
            record.get('hash', 'lost') + '.txt'
        )
        if not force and os.path.exists(full_text_path):
            return full_text_path
        if basename in files:
            with open(full_text_path, 'w') as output:
                output.write(full_text_from_pdf(files[basename]))
            return full_text_path

    @staticmethod
    def mappings_from_files(file_names, record_type,
                            full_text_path=None, force=False,
                            **kwargs):
        """
        Creates document mappings out of files.

        :param file_names: paths to the files
        :param record_type: type of record to extract
        :param kwargs: extra fields to include in the mappings
        :param full_text_path: path to look for full text pdf files
        :param force: force reading the full text from pdf files
        :return: an iterable over mappings
        """
        iterator_class = record_iterator_class(record_type)
        records = dict()
        if full_text_path:
            files = {
                os.path.basename(path): path
                for path in glob.glob(full_text_path + '**/*.pdf',
                                      recursive=True)
            }
        for file in tqdm(file_names, desc='processing files', unit='file'):
            progress_bar = tqdm(iterator_class(file), desc='processing records',
                                unit='record', leave=False)
            for record in progress_bar:
                record['keywords'] = '; '.join(record.get('keywords', ''))
                record.update(kwargs)
                records[record['hash']] = record
                if full_text_path:
                    record['full_text_path'] = Document.load_full_text(
                        record,
                        files,
                        force=force
                    )
        return [record for record in records.values()]

    @classmethod
    def list(cls, database, bibliography_eid, count=None):
        """
        Different to the usual list this one should just return records related to just
        one bibliography.
        """
        query = database.query(cls).filter(cls.bibliography_eid == bibliography_eid)
        if count is not None:
            query = query.limit(count)
        return query.all()

    @classmethod
    def count(cls, database, bibliography_eid):
        """
        Different to the usual count, it counts the number of documents in a given bibliography.
        """
        query = database.query(cls).filter(cls.bibliography_eid == bibliography_eid)
        return query.count()
