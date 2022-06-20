from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .meta import Base


class FeatureValue(Base):
    __tablename__ = 'feature_values'
    id = Column(Integer, primary_key=True)
    feature_id = Column(Integer, ForeignKey('features.id'))
    type_id = Column(Integer, ForeignKey('feature_value_types.id'))

    man_id = Column(String(20))
    name_en = Column(String(255))
    name_ru = Column(String(255))
    # Not adding 'comment' attributes here (corresponding to comment field in feature profiles)
    # because comments relate to an occurrence of a particular value
    # in a particular doculect - not to the abstract value itself

    type = relationship("FeatureValueType", back_populates="values")
    feature = relationship("Feature", back_populates="values")

    doculects = relationship(
        "Doculect", secondary='doculect_to_feature_value', back_populates="feature_values"
    )

    __table_args__ = (UniqueConstraint('feature_id', 'type_id', 'name_en', 'name_ru'),)
