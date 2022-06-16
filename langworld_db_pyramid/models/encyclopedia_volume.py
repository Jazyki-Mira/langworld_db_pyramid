from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship

from .meta import Base


class EncyclopediaVolume(Base):
    __tablename__ = 'encyclopedia_volumes'
    id = Column(Integer, primary_key=True)
    en = Column(Text)
    ru = Column(Text)
    file_name = Column(Text)
    pagenum_offset = Column(Integer)
    comment = Text
    doculects = relationship("Doculect", back_populates="encyclopedia_volume")
