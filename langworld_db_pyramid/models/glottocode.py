from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from .meta import Base


class Glottocode(Base):
    __tablename__ = 'glottocodes'
    id = Column(Integer, primary_key=True)
    code = Column(String(10))

    # Note that this is a many-to-many relationship. It is theoretically possible that not only one doculect
    # corresponds to many glottocodes, but that one glottocode corresponds to many doculects
    doculects = relationship('Doculect', back_populates='glottocodes', secondary='doculect_to_glottocode')
