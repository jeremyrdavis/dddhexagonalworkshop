from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

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

    def __init__(self, email: str):
        self.email = email

    def __repr__(self) -> str:
        return f"AttendeeEntity(id={self.id}, email='{self.email}')"
