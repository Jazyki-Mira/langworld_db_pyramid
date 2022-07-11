from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import backref, relationship

from .meta import Base


class Family(Base):
    __tablename__ = 'families'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('families.id'))
    man_id = Column(String(50))
    name_en = Column(String(255))
    name_ru = Column(String(255))

    children = relationship('Family', backref=backref('parent', remote_side=[id]))
    doculects = relationship('Doculect', back_populates='family')

    def has_doculects_with_feature_profiles(self) -> bool:
        """Checks recursively if this family or any of its children have doculects
        with feature profile filled out.
        """

        for doculect in self.doculects:
            if doculect.has_feature_profile:
                return True

        for child in self.children:
            if child.has_doculects_with_feature_profiles():
                return True

        return False
