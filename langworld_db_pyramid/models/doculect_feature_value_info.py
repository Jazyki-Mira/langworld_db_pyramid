from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from langworld_db_pyramid.models.meta import Base

# This class may seem to repeat the functionality of
# association_tables.DoculectToFeatureValue, but DoculectToFeatureValue
# is an auxiliary class used to automatically establish a relationship between two tables,
# while this one is used to add a comment to a specific feature value in a specific doculect.


class DoculectFeatureValueInfo(Base):
    """Class for giving additional info (comments, page numbers)
    to a specific feature value in a specific doculect."""

    __tablename__ = "additional_info_for_feature_values_in_doculects"
    doculect_id = Column(Integer, ForeignKey("doculects.id"), primary_key=True)
    feature_value_id = Column(Integer, ForeignKey("feature_values.id"), primary_key=True)

    page_numbers = Column(String(20))  # can be comma-separated numbers, not just single integer
    text_en = Column(Text)
    text_ru = Column(Text)

    doculect = relationship("Doculect", back_populates="feature_value_info_items")
    feature_value = relationship("FeatureValue", back_populates="doculect_comments")
