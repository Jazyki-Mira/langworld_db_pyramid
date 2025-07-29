from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from langworld_db_pyramid.models.meta import Base


class GrambankCode(Base):  # type: ignore[misc]
    __tablename__ = "grambank_codes"
    id = Column(Integer, primary_key=True)
    code = Column(String(10), index=True)  # Grambank codes are of the same length as glottocodes

    # Many-to-many relationship with Doculect
    doculects = relationship(
        "Doculect", back_populates="grambank_codes", secondary="doculect_to_grambank_code"
    )
