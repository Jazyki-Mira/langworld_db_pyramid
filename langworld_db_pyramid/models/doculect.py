from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    Text,
)

from .meta import Base


class Doculect(Base):
    __tablename__ = 'doculects'
    id = Column(Integer, primary_key=True)
    string_id = Column(Text)
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
    main_country_id = Column(Text)
    encyclopedia_volume_id = Column(Text)
    page = Column(Text)
    has_feature_profile = Column(Boolean)
    comment = Column(Text)
