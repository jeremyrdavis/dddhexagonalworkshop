# Step 3: Update the Attendee Aggregate

## TL;DR

Update `conference/attendees/domain/aggregates.py`:

```python
from conference.attendees.domain.events import AttendeeRegisteredEvent
from conference.attendees.domain.services import AttendeeRegistrationResult
from conference.attendees.domain.valueobjects import Address


class Attendee:
    def __init__(self, email: str, first_name: str, last_name: str, address: Address):
        self._email = email
        self._first_name = first_name
        self._last_name = last_name
        self._address = address

    @classmethod
    def register_attendee(
        cls, email: str, first_name: str, last_name: str, address: Address
    ) -> AttendeeRegistrationResult:
        attendee = cls(email, first_name, last_name, address)
        event = AttendeeRegisteredEvent(email=email, full_name=attendee.full_name)
        return AttendeeRegistrationResult(
            attendee=attendee,
            attendee_registered_event=event,
        )

    @property
    def email(self) -> str:
        return self._email

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def address(self) -> Address:
        return self._address

    @property
    def full_name(self) -> str:
        return f"{self._first_name} {self._last_name}"
```

[Step 4: Update the AttendeeRegisteredEvent](04-Update-the-Event.md)

## Overview

In this step, we update the `Attendee` aggregate to include first name, last name, and the `Address` value object. We also add a `full_name` computed property that demonstrates how aggregates can contain behavior, not just data.

## Learning Objectives

- Understand the difference between Aggregates, Entities, and Value Objects
- See how Value Objects compose into Aggregates
- Add business behavior to an Aggregate

## Value Objects vs. Entities vs. Aggregates

| Concept | Identity | Mutability | Example |
|---------|----------|------------|---------|
| **Value Object** | Defined by its attributes | Immutable | Address, Money, DateRange |
| **Entity** | Has a unique identifier | Mutable | Attendee (has email as identifier) |
| **Aggregate** | Cluster of entities and value objects | Root entity controls access | Attendee + Address |

The `Attendee` is the aggregate root. It owns the `Address` value object. External code should access the address through the attendee, not independently.

## Implementation

Update `conference/attendees/domain/aggregates.py` with the enhanced fields:

```python
from conference.attendees.domain.events import AttendeeRegisteredEvent
from conference.attendees.domain.services import AttendeeRegistrationResult
from conference.attendees.domain.valueobjects import Address


class Attendee:
    """
    An AGGREGATE is a cluster of associated objects that we treat as a unit
    for the purpose of data changes.
    -- Eric Evans, Domain-Driven Design, 2003
    """

    def __init__(self, email: str, first_name: str, last_name: str, address: Address):
        self._email = email
        self._first_name = first_name
        self._last_name = last_name
        self._address = address

    @classmethod
    def register_attendee(
        cls, email: str, first_name: str, last_name: str, address: Address
    ) -> AttendeeRegistrationResult:
        """Factory method that creates an Attendee and its registration event."""
        attendee = cls(email, first_name, last_name, address)
        event = AttendeeRegisteredEvent(email=email, full_name=attendee.full_name)
        return AttendeeRegistrationResult(
            attendee=attendee,
            attendee_registered_event=event,
        )

    @property
    def email(self) -> str:
        return self._email

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def address(self) -> Address:
        return self._address

    @property
    def full_name(self) -> str:
        return f"{self._first_name} {self._last_name}"
```

## Key Design Decisions

1. **`full_name` property**: The `full_name` property demonstrates how domain objects can contain behavior. The aggregate knows how to combine first and last names -- this is business logic that belongs in the domain, not in a controller or template.

2. **Factory method updated**: The `register_attendee` factory now accepts four parameters and passes the computed `full_name` to the event.

3. **Address is a Value Object**: The `Address` is stored as a private field with a read-only property. Because `Address` is frozen, it cannot be modified through the property.

## Next Step

Continue to [Step 4: Update the AttendeeRegisteredEvent](04-Update-the-Event.md)
