# Step 5: Update the Persistence Layer

## TL;DR

This step has three parts, so there is no short version. Read the full page.

## What We Are Building

In this step, we update the persistence layer to handle the new address fields. This demonstrates how to map complex domain objects to relational database structures while maintaining clean separation between domain and persistence concerns.

## The Object-Relational Impedance Mismatch

Earlier we said that Value Objects do not have an identity. In the logical sense, our `Address` does not have a unique identity of its own because it only exists as part of an `Attendee`.

However, we are choosing to model the `AddressEntity` as a separate table with a one-to-one mapping to our `AttendeeEntity`. Relational databases and Domain Objects do not always cleanly overlap, which is called [the object-relational impedance mismatch](https://en.wikipedia.org/wiki/Object%E2%80%93relational_impedance_mismatch).

The domain `Address` is a frozen dataclass with no `id` field. The persistence `AddressEntity` is a SQLAlchemy model with an auto-generated primary key. The repository handles the translation between the two.

## Step 5.1: Create the AddressEntity

Create `conference/attendees/persistence/address_entity.py`:

```python
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
```

## Step 5.2: Update the AttendeeEntity

Update `conference/attendees/persistence/entity.py` to add the new fields and a foreign key relationship to `AddressEntity`:

```python
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from conference.attendees.persistence.address_entity import AddressEntity
from database import Base


class AttendeeEntity(Base):
    __tablename__ = "attendee"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    address_id: Mapped[int] = mapped_column(ForeignKey("attendee_address.id"), nullable=False)
    address: Mapped[AddressEntity] = relationship(AddressEntity, cascade="all")

    def __init__(self, email: str, first_name: str, last_name: str, address: AddressEntity):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.address = address

    def __repr__(self) -> str:
        return f"AttendeeEntity(id={self.id}, email='{self.email}')"
```

Key points:

- `address_id` is a foreign key column pointing to the `attendee_address` table
- `address` is a SQLAlchemy relationship with `cascade="all"`, which ensures the address entity is persisted and deleted along with the attendee
- The constructor now requires `first_name`, `last_name`, and an `AddressEntity`

## Step 5.3: Update the AttendeeRepository

Update `conference/attendees/persistence/repository.py` to convert the domain `Address` value object into an `AddressEntity`:

```python
from sqlalchemy.orm import Session

from conference.attendees.domain.aggregates import Attendee
from conference.attendees.persistence.address_entity import AddressEntity
from conference.attendees.persistence.entity import AttendeeEntity


class AttendeeRepository:
    def __init__(self, session: Session):
        self._session = session

    def persist(self, aggregate: Attendee) -> None:
        entity = self._from_aggregate(aggregate)
        self._session.add(entity)
        self._session.flush()

    def _from_aggregate(self, attendee: Attendee) -> AttendeeEntity:
        address_entity = AddressEntity(
            street_address=attendee.address.street_address,
            bus=attendee.address.bus,
            postal_code=attendee.address.postal_code,
            town_or_municipality=attendee.address.town_or_municipality,
        )
        return AttendeeEntity(
            email=attendee.email,
            first_name=attendee.first_name,
            last_name=attendee.last_name,
            address=address_entity,
        )
```

The `_from_aggregate` method now creates an `AddressEntity` from the domain `Address` value object, then passes it to the `AttendeeEntity` constructor.

## Step 5.4: Update main.py

Add the `AddressEntity` import to `main.py` so SQLAlchemy creates the table on startup:

```python
from conference.attendees.persistence.address_entity import AddressEntity  # noqa: F401
from conference.attendees.persistence.entity import AttendeeEntity  # noqa: F401
```

## Database Schema

This will create two tables:

- `attendee`: Contains attendee information and a foreign key to address
- `attendee_address`: Contains address information

## Next Step

Continue to [Step 6: Update the AttendeeDTO](06-Update-the-DTO.md)
