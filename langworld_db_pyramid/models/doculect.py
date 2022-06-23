from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
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
    latitude = Column(String)
    longitude = Column(String)
    main_country_id = Column(Integer, ForeignKey('countries.id'))
    encyclopedia_volume_id = Column(Integer, ForeignKey('encyclopedia_volumes.id'))
    page = Column(Integer)
    has_feature_profile = Column(Boolean)
    comment_en = Column(Text)
    comment_ru = Column(Text)

    encyclopedia_volume = relationship("EncyclopediaVolume", back_populates="doculects")
    feature_value_comments = relationship('DoculectFeatureValueComment', back_populates='doculect')
    main_country = relationship("Country", back_populates="doculects")
    type = relationship("DoculectType", back_populates="doculects")

    # many-to-many relationships
    feature_values = relationship("FeatureValue", back_populates="doculects", secondary='doculect_to_feature_value')
    glottocodes = relationship('Glottocode', back_populates='doculects', secondary='doculect_to_glottocode')
    iso_639p3_codes = relationship('Iso639P3Code', back_populates='doculects', secondary='doculect_to_iso_639p3_code')
