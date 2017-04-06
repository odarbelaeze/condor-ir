import hashlib
import json
import os

import numpy

from sqlalchemy import Column, ForeignKey, Unicode
from sqlalchemy.orm import relationship

from condor.config import MODEL_PATH
from condor.models.base import AuditableMixing, DeclarativeBase
from condor.util import frequency


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
    
    @classmethod
    def lsa_from_term_document_matrix(cls, term_document_matrix, covariance):
        """Builds an lsa ranking matrix.
   
        This will ccut the matrix so taht it keeps the given covariance.
   
        :param term_document_matrix: term document matrix to use
        :param float covariance: amount of covariance to keep.
        :returns: the ranking matrix
        """
        u, s, v = numpy.linalg.svd(term_document_matrix.matrix,
                                   full_matrices=False)
        ss = s / numpy.sum(s)
        ss = numpy.cumsum(ss)
        k = numpy.sum(ss < covariance)
        bounded = numpy.dot(numpy.diag(s[:k]), v[:k, :])
        ranking = numpy.dot(u[:, :k], bounded)
        options = json.dumps({'covariance': covariance})

        unique_hash = hashlib.sha1(
            '{}{}'.format(term_document_matrix.matrix_path, options).encode()
        ).hexdigest()

        ranking_filename = os.path.join(MODEL_PATH, unique_hash + '.npy')
        numpy.save(ranking_filename, ranking)

        return cls(
            kind='lsa',
            build_options=options,
            ranking_matrix_path=ranking_filename,
            term_document_matrix_eid=term_document_matrix.eid
        )

    @property
    def matrix(self):
        return numpy.load(self.ranking_matrix_path)

    def query(self, tokens, limit=None, cosine=None):
        """
        Find the most relevant documents in the index given this tokens.

        The tokens are normalized and language guessed internally! So no
        worries, just pass in the tokens as entered by the user.

        :param tokens: query string to search
        :param limit: limit of documents to use
        :param cosine: limit cosine to use
        :return: list of documents
        """

        freq = frequency(self.term_document_matrix.words, tokens)

        if numpy.allclose(freq, 0):
            return []

        documents = self.term_document_matrix.bibliography.documents
        dot = numpy.dot(self.matrix, freq)
        norm_rank = numpy.linalg.norm(self.matrix, axis=1)
        norm_freq = numpy.linalg.norm(freq)
        cos = dot / (norm_rank * norm_freq)

        ordered = reversed(sorted(zip(documents, cos), key=lambda i: i[1]))

        if limit is None and cosine is None:
            limit = 10

        if cosine is not None:
            return [
                r for r in ordered
                if r[1] > cosine
            ]

        return list(ordered)[:limit]
