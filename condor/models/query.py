from sqlalchemy import Column, ForeignKey, Unicode
from sqlalchemy.orm import relationship

from condor.models.base import AuditableMixing, DeclarativeBase


class Query(AuditableMixing, DeclarativeBase):

    __tablename__ = 'query'

    bibliography_eid = Column(
        Unicode(40),
        ForeignKey('bibliography.eid')
    )

    contributor = Column(
        Unicode(40),
        nullable=True
    )

    topic = Column(
        Unicode(40),
        nullable=True
    )

    query_string = Column(
        Unicode(),
        nullable=False
    )

    bibliography = relationship(
        'Bibliography',
        back_populates='queries'
    )

    results = relationship(
        'QueryResult',
        back_populates='query'
    )

    def __repr__(self):
        return 'Query(eid={}, contributor={}, topic={}, query_string={})'.format(
            self.eid, self.contributor, self.topic, self.query_string
        )


class QueryResult(AuditableMixing, DeclarativeBase):

    __tablename__ = 'query_result'

    query_eid = Column(
        Unicode(40),
        ForeignKey('query.eid')
    )

    document_eid = Column(
        Unicode(40),
        ForeignKey('document.eid')
    )

    query = relationship(
        'Query',
        back_populates='results'
    )

    document = relationship('Document')

    def __repr__(self):
        return 'Query(query={}, document={})'.format(
            self.query, self.document
        )
