from sqlalchemy import Column, ForeignKey

from .meta import Base


class DoculectToFeatureValue(Base):
    """Class for **automatic** creation of objects by SQLAlchemy
    when establishing "many to many" relationship
    between `Doculect` and `FeatureValue`.
    """
    __tablename__ = 'doculect_to_feature_value'
    doculect_id = Column(ForeignKey('doculects.id'), primary_key=True)
    feature_value_id = Column(ForeignKey('feature_values.id'), primary_key=True)


class DoculectToGlottocode(Base):
    """Class for **automatic** creation of objects by SQLAlchemy
    when establishing "many to many" relationship
    between `Doculect` and `Glottocode`.
    """
    __tablename__ = 'doculect_to_glottocode'
    doculect_id = Column(ForeignKey('doculects.id'), primary_key=True)
    glottocode_id = Column(ForeignKey('glottocodes.id'), primary_key=True)


class DoculectToIso639P3Code(Base):
    """Class for **automatic** creation of objects by SQLAlchemy
    when establishing "many to many" relationship
    between `Doculect` and `Iso639P3Code`.
    """
    __tablename__ = 'doculect_to_iso_639p3_code'
    doculect_id = Column(ForeignKey('doculects.id'), primary_key=True)
    iso_639p3_code_id = Column(ForeignKey('iso_639p3_codes.id'), primary_key=True)
