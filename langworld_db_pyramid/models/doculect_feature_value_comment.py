from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from langworld_db_pyramid.models.meta import Base


# This class may seem to repeat the functionality of
# association_tables.DoculectToFeatureValue, but DoculectToFeatureValue
# is an auxiliary class used to automatically establish a relationship between two tables,
# while this one is used to add a comment to a specific feature value in a specific doculect.

class DoculectFeatureValueComment(Base):
    """Class for adding comments
    to a specific feature value in a specific doculect."""

    __tablename__ = 'comments_for_feature_values_in_doculects'
    doculect_id = Column(Integer, ForeignKey('doculects.id'), primary_key=True)
    feature_value_id = Column(Integer, ForeignKey('feature_values.id'), primary_key=True)

    text_en = Column(Text)
    text_ru = Column(Text)

    doculect = relationship('Doculect', back_populates='feature_value_comments')
    feature_value = relationship('FeatureValue', back_populates='doculect_comments')
