from sqlalchemy import Column, ForeignKey, Text

from .meta import Base


# TODO rename module?
class DoculectToFeatureValue(Base):
    __tablename__ = 'doculect_to_feature_value'
    doculect_id = Column(ForeignKey('doculects.id'), primary_key=True)
    feature_value_id = Column(ForeignKey('feature_values.id'), primary_key=True)
    comment_en = Column(Text)
    comment_ru = Column(Text)
