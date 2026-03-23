from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class AddressEntity(Base):
    """
    Persistence entity for Address data. Separate from the domain value object.

    Unlike the domain Address (which has no identity), the database entity
    requires a primary key. This is the object-relational impedance mismatch
    that the persistence layer handles.
    """

    __tablename__ = "attendee_address"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    street_address: Mapped[str] = mapped_column(String, nullable=False)
    bus: Mapped[str | None] = mapped_column(String, nullable=True)
    postal_code: Mapped[str] = mapped_column(String, nullable=False)
    town_or_municipality: Mapped[str] = mapped_column(String, nullable=False)

    def __init__(self, street_address: str, bus: str | None, postal_code: str, town_or_municipality: str):
        self.street_address = street_address
        self.bus = bus
        self.postal_code = postal_code
        self.town_or_municipality = town_or_municipality

    def __repr__(self) -> str:
        return f"AddressEntity(id={self.id}, street='{self.street_address}')"
