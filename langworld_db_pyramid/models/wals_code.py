from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from langworld_db_pyramid.models.meta import Base


class WalsCode(Base):  # type: ignore[misc]
    __tablename__ = "wals_codes"
    id = Column(Integer, primary_key=True)
    code = Column(String(3), index=True)  # WALS codes are 3 characters long (e.g., "rus")

    # Note that this is a many-to-many relationship. It is theoretically possible that not only one
    # doculect corresponds to many WALS codes, but that one WALS code corresponds to many
    # doculects.
    doculects = relationship(
        "Doculect", back_populates="wals_codes", secondary="doculect_to_wals_code"
    )
