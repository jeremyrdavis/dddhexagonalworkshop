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

    # TODO: Add street_address, bus, postal_code, town_or_municipality columns
