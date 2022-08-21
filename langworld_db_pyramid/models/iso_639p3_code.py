from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from .meta import Base


class Iso639P3Code(Base):
    __tablename__ = 'iso_639p3_codes'
    id = Column(Integer, primary_key=True)
    code = Column(String(3), index=True)

    # Note that this is a many-to-many relationship. It is theoretically possible that not only one doculect
    # corresponds to many ISO-639-3 codes, but that one ISO-639-3 corresponds to many doculects.
    doculects = relationship('Doculect', back_populates='iso_639p3_codes', secondary='doculect_to_iso_639p3_code')
