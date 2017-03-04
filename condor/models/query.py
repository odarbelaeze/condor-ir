from sqlalchemy import Column, ForeignKey, Unicode
from sqlalchemy.orm import relationship

from condor.models.base import AuditableMixing, DeclarativeBase


class Query(AuditableMixing, DeclarativeBase):

    __tablename__ = 'query'

    bibliography_set_eid = Column(
        Unicode(40),
        ForeignKey('bibliography_set.eid')
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

    bibliography_set = relationship(
        'BibliographySet',
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

    bibliography_eid = Column(
        Unicode(40),
        ForeignKey('bibliography.eid')
    )

    query = relationship(
        'Query',
        back_populates='results'
    )

    bibliography = relationship('Bibliography')

    def __repr__(self):
        return 'Query(query={}, bibliography={})'.format(
            self.query, self.bibliography
        )
