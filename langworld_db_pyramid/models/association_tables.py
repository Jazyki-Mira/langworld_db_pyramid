from sqlalchemy import Column, ForeignKey

from .meta import Base


class DoculectToFeatureValue(Base):
    """Class for **automatic** creation of objects by SQLAlchemy
    when establishing "many to many" relationship
    between Doculect and FeatureValue.
    """
    __tablename__ = 'doculect_to_feature_value'
    doculect_id = Column(ForeignKey('doculects.id'), primary_key=True)
    feature_value_id = Column(ForeignKey('feature_values.id'), primary_key=True)
