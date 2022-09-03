from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from langworld_db_pyramid.models.meta import Base


class FeatureValueType(Base):
    __tablename__ = 'feature_value_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    entails_empty_value = Column(Boolean)

    values = relationship("FeatureValue", back_populates="type")
