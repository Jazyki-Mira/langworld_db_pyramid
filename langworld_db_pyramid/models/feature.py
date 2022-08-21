from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from .meta import Base


class Feature(Base):
    __tablename__ = 'features'
    id = Column(Integer, primary_key=True)
    man_id = Column(String(10), index=True)
    category_id = Column(Integer, ForeignKey('feature_categories.id'))
    name_en = Column(String(100))
    name_ru = Column(String(100))

    category = relationship("FeatureCategory", back_populates="features")
    values = relationship("FeatureValue", back_populates="feature")
