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
