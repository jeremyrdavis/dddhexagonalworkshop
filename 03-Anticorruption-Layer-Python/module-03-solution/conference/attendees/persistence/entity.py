from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from conference.attendees.persistence.address_entity import AddressEntity
from database import Base


class AttendeeEntity(Base):
    """
    Persistence entity for Attendee data. Separate from the domain aggregate.

    The entity handles database mapping concerns while the aggregate handles
    business logic. This separation is a key principle of Hexagonal Architecture.
    """

    __tablename__ = "attendee"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    address_id: Mapped[int | None] = mapped_column(ForeignKey("attendee_address.id"), nullable=True)
    address: Mapped[AddressEntity | None] = relationship(AddressEntity, cascade="all")

    def __init__(self, email: str, first_name: str, last_name: str, address: AddressEntity | None = None):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.address = address

    def __repr__(self) -> str:
        return f"AttendeeEntity(id={self.id}, email='{self.email}')"
