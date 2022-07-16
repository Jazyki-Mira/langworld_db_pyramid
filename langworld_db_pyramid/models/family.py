from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
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

    def has_doculects_with_feature_profiles(self) -> bool:  # TODO test
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

    def iter_doculects_that_have_feature_profiles(self):  # TODO test
        if not self.has_doculects_with_feature_profiles():
            return []

        yield from (d for d in self.doculects if d.has_feature_profile)

        for child in self.children:
            yield from child.iter_doculects_that_have_feature_profiles()
