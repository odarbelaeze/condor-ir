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
