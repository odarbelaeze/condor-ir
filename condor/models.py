import hashlib
import uuid

from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Unicode,
)


DeclarativeBase = declarative_base()


def eid_gen():
    sha = hashlib.sha1('{}'.format(uuid.uuid4()).encode())
    return sha.hexdigest()


class AuditableMixing(object):
    """
    Table mixing to add the common fields in our database, to make it auditable
    we add timestamps and an eid field as primary key just for convenience.
    """

    eid = Column(Unicode(40), primary_key=True, default=eid_gen)
    created = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    modified = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


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