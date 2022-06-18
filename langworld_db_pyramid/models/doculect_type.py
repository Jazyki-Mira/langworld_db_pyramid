from sqlalchemy import (
    Column,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship

from .meta import Base


class DoculectType(Base):
    __tablename__ = 'doculect_types'
    id = Column(Integer, primary_key=True)
    name_en = Column(Text)
    name_ru = Column(Text)
    doculects = relationship("Doculect", back_populates="type")
