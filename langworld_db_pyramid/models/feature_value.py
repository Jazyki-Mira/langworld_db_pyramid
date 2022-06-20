from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from .association_tables import doculect_to_feature_value
from .meta import Base


class FeatureValue(Base):
    __tablename__ = 'feature_values'
    id = Column(Integer, primary_key=True)
    man_id = Column(String(20))
    feature_id = Column(Integer, ForeignKey('features.id'))
    name_en = Column(String(255))
    name_ru = Column(String(255))

    feature = relationship("Feature", back_populates="values")
    doculects = relationship(
        "Doculect", secondary=doculect_to_feature_value, back_populates="feature_values"
    )
