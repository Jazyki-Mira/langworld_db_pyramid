from typing import Iterable
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
    man_id = Column(String(50), index=True)
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

    def is_descendant_of(self, man_id_of_presumable_parent: str) -> bool:
        """Checks if this family has a family with given man_id
        as its ancestor.
        Goes recursively up the genealogy tree.
        """
        if self.parent is None:
            return False
        if self.parent.man_id == man_id_of_presumable_parent:
            return True
        return self.parent.is_descendant_of(man_id_of_presumable_parent)

    def iter_doculects_that_have_feature_profiles(self) -> Iterable:
        if not self.has_doculects_with_feature_profiles():
            return []

        yield from (d for d in self.doculects if d.has_feature_profile)

        for child in self.children:
            yield from child.iter_doculects_that_have_feature_profiles()
