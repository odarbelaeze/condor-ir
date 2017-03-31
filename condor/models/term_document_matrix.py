"""
Just a normal text document matrix representation, the actual matrix is
stored off site on a numpy file.
"""
import hashlib
import os

import numpy
from nltk import collections

from sqlalchemy import Column, ForeignKey, Unicode
from sqlalchemy.orm import relationship

from condor.config import MATRIX_PATH, TERM_LIST_PATH
from condor.models.base import AuditableMixing, DeclarativeBase
from condor.normalize import CompleteNormalizer


class TermDocumentMatrix(AuditableMixing, DeclarativeBase):
    """
    Represents a term document matrix.
    """

    __tablename__ = 'term_document_matrix'

    bibliography_set_eid = Column(
        Unicode(40),
        ForeignKey('bibliography_set.eid')
    )

    bibliography_options = Column(Unicode(512), nullable=False)
    processing_options = Column(Unicode(512), nullable=False)
    term_list_path = Column(Unicode(512), nullable=False)
    matrix_path = Column(Unicode(512), nullable=False)

    bibliography_set = relationship(
        'BibliographySet',
        back_populates='term_document_matrices',
    )

    ranking_matrices = relationship(
        'RankingMatrix',
        back_populates='term_document_matrix',
        cascade='all, delete-orphan',
    )

    @classmethod
    def from_bibliography_set(cls, bibliography_set, regularise=True,
                              fields=None, normalizer_class=None):
        """
        Build a matrix from a bibliography set.

        This has the side effect of creating the matrix a and terms files.

        :param bibliography_set: a bibliography set
        :param regularise: apply TF IDF regularization.
        :param fields: fields of interest
        :param normalizer_class: normalizer class to use
        :return: a term document matrix.
        """
        fields = fields or ['title', 'description', 'keywords']
        normalizer_class = normalizer_class or CompleteNormalizer
        words = bibliography_set.words(fields=fields,
                                       normalizer_class=CompleteNormalizer)
        frequency = numpy.zeros(
            (len(bibliography_set.bibliographies), len(words)),
            dtype=int
        )
        for row, col, freq in cls._matrix(words,
                                          bibliography_set,
                                          fields,
                                          normalizer_class):
            frequency[row][col] = freq

        if regularise:
            tf = (frequency.T / numpy.sum(frequency, axis=1)).T
            df = numpy.sum(frequency > 0, axis=0)
            idf = numpy.log(len(bibliography_set.bibliographies) / df) + 1
            frequency = tf * idf

        unique_hash = hashlib.sha1(
            '{}{}{}{}'.format(
                ''.join(words),
                ''.join(fields),
                normalizer_class.__mro__,
                regularise
            ).encode()
        ).hexdigest()
        matrix_filename = os.path.join(MATRIX_PATH, unique_hash + '.npy')
        words_filename = os.path.join(TERM_LIST_PATH, unique_hash + '.txt')
        numpy.save(matrix_filename, frequency)
        with open(words_filename, 'w') as file:
            file.write('\n'.join(words))
        return cls(
            bibliography_options='',
            processing_options=str(normalizer_class.__mro__),
            term_list_path=words_filename,
            matrix_path=matrix_filename,
            bibliography_set_eid=bibliography_set.eid
        )

    @staticmethod
    def _matrix(words, bibliography_set, fields, normalizer_class):
        word_dict = {word: pos for pos, word in enumerate(words)}
        for ind, bib in enumerate(bibliography_set.bibliographies):
            raw = bib.raw_data(fields, normalizer_class)
            frequency = collections.Counter(raw)
            for word, freq in frequency.items():
                yield ind, word_dict[word], freq

    @property
    def words(self):
        """
        Load the words stored off site.
        """
        with open(self.term_list_path) as term_file:
            terms = term_file.read().split('\n')
        return terms

    @property
    def matrix(self):
        """
        Load the matrix stored off site.
        """
        return numpy.load(self.matrix_path)
