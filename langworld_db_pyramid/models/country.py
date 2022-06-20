from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from .meta import Base


class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True)
    man_id = Column(String(3))
    iso = Column(String(3))
    is_historical = Column(Boolean)
    name_en = Column(String(100))
    name_ru = Column(String(100))
    doculects = relationship("Doculect", back_populates="main_country")
