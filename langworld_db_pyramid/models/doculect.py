from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from .meta import Base


class Doculect(Base):
    __tablename__ = 'doculects'
    id = Column(Integer, primary_key=True)
    man_id = Column(String(100))
    type_id = Column(ForeignKey('doculect_types.id'))
    is_extinct = Column(Boolean)
    is_multiple = Column(Boolean)
    name_en = Column(String(255))
    name_ru = Column(String(255))
    custom_title_en = Column(String(255))
    custom_title_ru = Column(String(255))
    aliases_en = Column(String)
    aliases_ru = Column(String)
    family_id = Column(String(50))
    iso_639_3 = Column(String)
    glottocode = Column(String)
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    main_country_id = Column(Integer, ForeignKey('countries.id'))
    encyclopedia_volume_id = Column(Integer, ForeignKey('encyclopedia_volumes.id'))
    page = Column(Integer)
    has_feature_profile = Column(Boolean)
    comment = Column(Text)

    type = relationship("DoculectType", back_populates="doculects")
    encyclopedia_volume = relationship("EncyclopediaVolume", back_populates="doculects")
    feature_values = relationship(
        "FeatureValue", secondary='doculect_to_feature_value', back_populates="doculects"
    )
    main_country = relationship("Country", back_populates="doculects")
