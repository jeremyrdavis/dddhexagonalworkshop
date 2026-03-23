# Step 1: Create the Address Value Object

## TL;DR

Create `conference/attendees/domain/valueobjects.py`:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Address:
    street_address: str
    bus: str | None
    postal_code: str
    town_or_municipality: str

    def __post_init__(self):
        if not self.street_address or self.street_address.strip() == "":
            raise ValueError("Street address cannot be null or blank")
        if not self.postal_code or self.postal_code.strip() == "":
            raise ValueError("Postal code cannot be null or blank")
        if not self.town_or_municipality or self.town_or_municipality.strip() == "":
            raise ValueError("City cannot be null or blank")
```

[Step 2: Update the RegisterAttendeeCommand](02-Update-the-Command.md)

## Learning Objectives

- Understand the difference between Value Objects and Entities
- Implement an `Address` Value Object using Python's frozen dataclasses
- Add validation to enforce business invariants

## Why Value Objects Matter

Value Objects are objects that describe the state of something else. They are not Entities, which have continuity and identify something that is tracked over time.

- **Value Objects** are equal based on their **value**
- **Entities** are equal based on their **identifier**

Consider an address: "1 Bag End, Hobbiton, 12345" is the same address regardless of where it appears. Two `Address` objects with the same fields are interchangeable. There is no separate "address ID" that distinguishes one from another in the domain. This makes `Address` a Value Object.

Contrast this with an `Attendee`, which has continuity over time. Even if two attendees share the same name, they are different people with different registration histories.

## Implementation

The `Address` Value Object lives in the domain layer, in a new file: `conference/attendees/domain/valueobjects.py`.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Address:
    """
    A VALUE OBJECT is an object that describes some characteristic or attribute
    but carries no concept of identity.
    -- Eric Evans, Domain-Driven Design, 2003

    Value objects are defined by their attributes, not by an identity.
    Two addresses with the same fields are the same address.
    """

    street_address: str
    bus: str | None
    postal_code: str
    town_or_municipality: str

    def __post_init__(self):
        if not self.street_address or self.street_address.strip() == "":
            raise ValueError("Street address cannot be null or blank")
        if not self.postal_code or self.postal_code.strip() == "":
            raise ValueError("Postal code cannot be null or blank")
        if not self.town_or_municipality or self.town_or_municipality.strip() == "":
            raise ValueError("City cannot be null or blank")
```

### Why `@dataclass(frozen=True)`?

Value Objects should be immutable. Once created, they should never change. If you need a different address, you create a new one.

The `frozen=True` parameter enforces this at runtime:

- All fields become read-only. Attempting to assign a new value raises `FrozenInstanceError`.
- `__eq__` and `__hash__` are generated automatically, so two addresses with the same data are considered equal.
- This mirrors Java records, which are used for Value Objects in the Java version of this workshop.

### Why validation in `__post_init__`?

Value Objects should be self-validating. An `Address` without a street or city is not a valid address, and the domain model should never allow one to exist. The `__post_init__` method runs after `__init__` and raises `ValueError` if any required field is missing or blank.

Note that `bus` (apartment, suite, unit number) is optional -- not every address has one.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `street_address` | `str` | Yes | Street name and number |
| `bus` | `str \| None` | No | Apartment, suite, or unit number |
| `postal_code` | `str` | Yes | Postal or ZIP code |
| `town_or_municipality` | `str` | Yes | City or town name |

## Testing Your Implementation

Create `tests/domain/test_valueobjects.py`:

```python
import dataclasses

import pytest

from conference.attendees.domain.valueobjects import Address


class TestAddress:
    def test_address_creation(self):
        address = Address(
            street_address="1 Bag End",
            bus=None,
            postal_code="12345",
            town_or_municipality="Hobbiton",
        )
        assert address.street_address == "1 Bag End"
        assert address.bus is None
        assert address.postal_code == "12345"
        assert address.town_or_municipality == "Hobbiton"

    def test_address_is_immutable(self):
        address = Address(
            street_address="1 Bag End",
            bus=None,
            postal_code="12345",
            town_or_municipality="Hobbiton",
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            address.street_address = "2 Bag End"

    def test_address_equality(self):
        address1 = Address(
            street_address="1 Bag End",
            bus=None,
            postal_code="12345",
            town_or_municipality="Hobbiton",
        )
        address2 = Address(
            street_address="1 Bag End",
            bus=None,
            postal_code="12345",
            town_or_municipality="Hobbiton",
        )
        assert address1 == address2

    def test_address_rejects_blank_street(self):
        with pytest.raises(ValueError, match="Street address cannot be null or blank"):
            Address(
                street_address="",
                bus=None,
                postal_code="12345",
                town_or_municipality="Hobbiton",
            )
```

Run the tests:

```bash
pytest tests/domain/test_valueobjects.py -v
```

## Next Step

Continue to [Step 2: Update the RegisterAttendeeCommand](02-Update-the-Command.md)
