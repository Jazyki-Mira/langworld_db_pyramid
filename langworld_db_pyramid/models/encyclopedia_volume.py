from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from langworld_db_pyramid.models.meta import Base


class EncyclopediaVolume(Base):
    __tablename__ = 'encyclopedia_volumes'
    id = Column(Integer, primary_key=True)
    en = Column(String(255))
    ru = Column(String(255))
    file_name = Column(String(255))
    pagenum_offset = Column(Integer)
    comment = Column(Text)
    doculects = relationship("Doculect", back_populates="encyclopedia_volume")
