from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship

from .meta import Base


class Feature(Base):
    __tablename__ = 'features'
    id = Column(Integer, primary_key=True)
    man_id = Column(Text)
    category_id = Column(Integer, ForeignKey('feature_categories.id'))
    name_en = Column(Text)
    name_ru = Column(Text)

    category = relationship("FeatureCategory", back_populates="features")
    values = relationship("FeatureValue", back_populates="feature")
