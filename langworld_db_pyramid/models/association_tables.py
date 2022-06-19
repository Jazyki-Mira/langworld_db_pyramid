from sqlalchemy import Column, ForeignKey, Table

from .meta import Base

doculect_to_feature_value = Table(
    'doculect_to_feature_value',
    Base.metadata,
    Column('doculect_id', ForeignKey('doculects.id'), primary_key=True),
    Column('feature_value_id', ForeignKey('feature_values.id'), primary_key=True),
)
