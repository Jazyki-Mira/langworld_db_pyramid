from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from langworld_db_pyramid.models.meta import Base


class FeatureValue(Base):
    __tablename__ = 'feature_values'
    id = Column(Integer, primary_key=True)
    feature_id = Column(Integer, ForeignKey('features.id'))
    type_id = Column(Integer, ForeignKey('feature_value_types.id'))

    man_id = Column(String(20), index=True)
    name_en = Column(String(255))
    name_ru = Column(String(255))
    # Not adding 'comment' attributes here (corresponding to comment field in feature profiles)
    # because comments relate to an occurrence of a particular value
    # in a particular doculect - not to the abstract value itself

    # Values for this column must be calculated after the database is filled with doculects
    # This may not be optimal, but it speeds up the rendering of query wizard significantly
    # because the expensive filtering no longer has to be done at rendering time.
    is_listed_and_has_doculects = Column(Boolean)

    doculects = relationship('Doculect', secondary='doculect_to_feature_value', back_populates='feature_values')
    doculect_comments = relationship('DoculectFeatureValueComment', back_populates='feature_value')
    feature = relationship('Feature', back_populates='values')
    type = relationship('FeatureValueType', back_populates='values')

    __table_args__ = (UniqueConstraint('feature_id', 'type_id', 'name_en', 'name_ru'), )
