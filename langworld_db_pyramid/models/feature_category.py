from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship

from .meta import Base


class FeatureCategory(Base):
    __tablename__ = 'feature_categories'
    id = Column(Integer, primary_key=True)
    man_id = Column(Text)
    name_en = Column(Text)
    name_ru = Column(Text)
    features = relationship("Feature", back_populates="category")
