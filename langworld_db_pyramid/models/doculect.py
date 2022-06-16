from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship

from .meta import Base


class Doculect(Base):
    __tablename__ = 'doculects'
    id = Column(Integer, primary_key=True)
    man_id = Column(Text)
    type = Column(Text)
    is_extinct = Column(Boolean)
    is_multiple = Column(Boolean)
    name_en = Column(Text)
    name_ru = Column(Text)
    custom_title_en = Column(Text)
    custom_title_ru = Column(Text)
    aliases_en = Column(Text)
    aliases_ru = Column(Text)
    family_id = Column(Text)
    iso_639_3 = Column(Text)
    glottocode = Column(Text)
    latitude = Column(Text)
    longitude = Column(Text)
    main_country_id = Column(Integer, ForeignKey('countries.id'))
    encyclopedia_volume_id = Column(Text, ForeignKey('encyclopedia_volumes.id'))
    page = Column(Text)
    has_feature_profile = Column(Boolean)
    comment = Column(Text)
    main_country = relationship("Country", back_populates="doculects")
    encyclopedia_volume = relationship("EncyclopediaVolume", back_populates="doculects")
