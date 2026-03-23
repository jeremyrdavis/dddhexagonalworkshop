# Step 2: Update the RegisterAttendeeCommand

## TL;DR

Update the `RegisterAttendeeCommand` in `conference/attendees/domain/services.py`:

```python
from conference.attendees.domain.valueobjects import Address

@dataclass(frozen=True)
class RegisterAttendeeCommand:
    email: str
    first_name: str
    last_name: str
    address: Address

    def __post_init__(self):
        if not self.email or self.email.strip() == "":
            raise ValueError("Email cannot be null or blank")
        if "@" not in self.email:
            raise ValueError("Email must contain @ symbol")
        if not self.first_name or self.first_name.strip() == "":
            raise ValueError("First name cannot be null or blank")
        if not self.last_name or self.last_name.strip() == "":
            raise ValueError("Last name cannot be null or blank")
        if self.address is None:
            raise ValueError("Address cannot be null")
```

[Step 3: Update the Attendee Aggregate](03-Update-the-Aggregate.md)

## Overview

In this step, we update the `RegisterAttendeeCommand` to include the new `Address` value object along with first and last name fields. This demonstrates how commands evolve to capture new business requirements while maintaining the command pattern.

## Understanding Commands in DDD

Commands represent the intent to change the state of the system. They:

- Capture user intentions
- Contain all data needed to perform an operation
- Are immutable once created
- Can fail or be rejected (unlike events, which represent facts)

## Implementation

Update the `RegisterAttendeeCommand` in `conference/attendees/domain/services.py`. Add the `Address` import to the `TYPE_CHECKING` block and update the dataclass:

```python
if TYPE_CHECKING:
    from conference.attendees.domain.aggregates import Attendee
    from conference.attendees.domain.valueobjects import Address
    from conference.attendees.infrastructure.dto import AttendeeDTO
    from conference.attendees.infrastructure.event_publisher import AttendeeEventPublisher
    from conference.attendees.persistence.repository import AttendeeRepository
```

Then update the command:

```python
@dataclass(frozen=True)
class RegisterAttendeeCommand:
    """
    Commands encapsulate the intent to perform a business operation.
    Unlike events, commands can fail or be rejected.
    """

    email: str
    first_name: str
    last_name: str
    address: Address

    def __post_init__(self):
        if not self.email or self.email.strip() == "":
            raise ValueError("Email cannot be null or blank")
        if "@" not in self.email:
            raise ValueError("Email must contain @ symbol")
        if not self.first_name or self.first_name.strip() == "":
            raise ValueError("First name cannot be null or blank")
        if not self.last_name or self.last_name.strip() == "":
            raise ValueError("Last name cannot be null or blank")
        if self.address is None:
            raise ValueError("Address cannot be null")
```

## Key Changes

1. **Added `first_name` and `last_name` fields**: Instead of relying solely on email, we now capture the attendee's name
2. **Added `address` value object**: The command includes the complete address encapsulated in our `Address` value object
3. **Added validation**: New fields are validated in `__post_init__` to ensure they are not blank
4. **Maintained immutability**: The `frozen=True` parameter ensures the command remains immutable

## Note on the Address Import

The `Address` import is inside the `TYPE_CHECKING` block because of Python's circular import handling. At runtime, Python resolves the type via `from __future__ import annotations` (which makes all annotations strings). The import only runs during static type checking.

## Next Step

Continue to [Step 3: Update the Attendee Aggregate](03-Update-the-Aggregate.md)
