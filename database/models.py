from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship, validates
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy_serializer import SerializerMixin

Base = declarative_base()


class City(Base, SerializerMixin):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    normalized_name: Mapped[str] = mapped_column(String(120))
    state_abbreviation: Mapped[str] = mapped_column(String(2))

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=datetime.utcnow)
    logs: Mapped[List["CityLog"]] = relationship(back_populates="city")

    __table_args__ = (UniqueConstraint("name", "state_abbreviation", name="name_state_uc"),)

    @validates("state_abbreviation")
    def validate_state_abbreviation(self, key, value):
        if not value.isalpha() or not value.isupper() or len(value) != 2:
            raise ValueError("State abbreviation must be a two-letter uppercase string")
        return value

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id} - {self.name} - {self.state_abbreviation}>"


class CityLogStatus(Enum):
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"
    SELECTED = "selected"


class CityLog(Base, SerializerMixin):
    __tablename__ = "city_log"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    status: Mapped[CityLogStatus]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    city: Mapped["City"] = relationship("City", back_populates="logs")

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id} - City ID: {self.city_id} - Status: {self.status.value} - Created At: {self.created_at}>"
