from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from langworld_db_pyramid.dbutils.query_mixin import QueryMixin
from langworld_db_pyramid.models.meta import Base


class Doculect(QueryMixin, Base):  # type: ignore[misc]
    __tablename__ = "doculects"
    id = Column(Integer, primary_key=True)
    man_id = Column(String(100), index=True)
    type_id = Column(ForeignKey("doculect_types.id"))
    is_extinct = Column(Boolean)
    is_multiple = Column(Boolean)
    name_en = Column(String(255), index=True)
    name_ru = Column(String(255), index=True)
    custom_title_en = Column(String(255))
    custom_title_ru = Column(String(255))
    # Aliases could be in a separate table, but they are not organized as pairs of English and
    # Russian equivalents, which would mean separate tables (one per locale) or more complex
    # queries.  So far I don't think it's worth it.
    aliases_en = Column(String, index=True)
    aliases_ru = Column(String, index=True)
    family_id = Column(Integer, ForeignKey("families.id"))
    latitude = Column(String)
    longitude = Column(String)
    main_country_id = Column(Integer, ForeignKey("countries.id"))
    encyclopedia_volume_id = Column(Integer, ForeignKey("encyclopedia_volumes.id"))
    page = Column(Integer)
    has_feature_profile = Column(Boolean, index=True)
    comment_en = Column(Text)
    comment_ru = Column(Text)

    encyclopedia_volume = relationship("EncyclopediaVolume", back_populates="doculects")
    family = relationship("Family", back_populates="doculects")
    feature_value_info_items = relationship("DoculectFeatureValueInfo", back_populates="doculect")
    main_country = relationship("Country", back_populates="doculects")
    type = relationship("DoculectType", back_populates="doculects")

    # many-to-many relationships
    encyclopedia_maps = relationship(
        "EncyclopediaMap", back_populates="doculects", secondary="encyclopedia_map_to_doculect"
    )
    feature_values = relationship(
        "FeatureValue", back_populates="doculects", secondary="doculect_to_feature_value"
    )
    glottocodes = relationship(
        "Glottocode", back_populates="doculects", secondary="doculect_to_glottocode"
    )
    grambank_codes = relationship(
        "GrambankCode", back_populates="doculects", secondary="doculect_to_grambank_code"
    )
    iso_639p3_codes = relationship(
        "Iso639P3Code", back_populates="doculects", secondary="doculect_to_iso_639p3_code"
    )
    wals_codes = relationship(
        "WalsCode", back_populates="doculects", secondary="doculect_to_wals_code"
    )

    def belongs_to_family(self, family_man_id: str) -> bool:
        """Recursively (goes up the genealogy) checks
        if doculect belongs to a family with a given man_id."""
        # calling method of Family may look like violating Demeter law, but Family
        # is immediately related to Doculect
        return self.family.man_id == family_man_id or self.family.is_descendant_of(family_man_id)
