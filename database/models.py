from datetime import datetime
from typing import Optional

from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy_serializer import SerializerMixin

Base = declarative_base()


class City(Base, SerializerMixin):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    state_abbreviation: Mapped[str] = mapped_column(String(2), nullable=False)

    created: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated: Mapped[Optional[datetime]] = mapped_column(onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint("name", "state_abbreviation", name="name_state_uc"),)

    @validates("state_abbreviation")
    def validate_state_abbreviation(self, key, value):
        if not value.isalpha() or not value.isupper() or len(value) != 2:
            raise ValueError("State abbreviation must be a two-letter uppercase string")
        return value

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id} - {self.name} - {self.state_abbreviation}>"
