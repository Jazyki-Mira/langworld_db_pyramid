from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from .meta import Base


class FeatureValueType(Base):
    __tablename__ = 'feature_value_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))

    values = relationship("FeatureValue", back_populates="type")
