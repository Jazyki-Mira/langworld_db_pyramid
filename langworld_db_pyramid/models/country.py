from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship

from .meta import Base


class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True)
    man_id = Column(Text)
    iso = Column(Text)
    is_historical = Column(Boolean)
    name_en = Column(Text)
    name_ru = Column(Text)
    doculects = relationship("Doculect", back_populates="main_country")
