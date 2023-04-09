from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from langworld_db_pyramid.models.meta import Base


class EncyclopediaMap(Base):  # type: ignore[misc]
    __tablename__ = "encyclopedia_maps"
    id = Column(Integer, primary_key=True)
    man_id = Column(String(10))
    en = Column(String(255))
    ru = Column(String(255))
    file_name = Column(String(255))
    comment = Column(Text)
    doculects = relationship(
        "Doculect", back_populates="encyclopedia_maps", secondary="encyclopedia_map_to_doculect"
    )
