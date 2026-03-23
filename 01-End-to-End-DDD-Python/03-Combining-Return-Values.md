# Step 3: Combining Return Values

**Note:** This step is not specific to Domain-Driven Design. This is simply a useful coding practice.

## TL;DR

Add the `AttendeeRegistrationResult` to `conference/attendees/domain/services.py`, below the `RegisterAttendeeCommand` you created in Step 2:

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from conference.attendees.domain.aggregates import Attendee

from conference.attendees.domain.events import AttendeeRegisteredEvent


@dataclass(frozen=True)
class AttendeeRegistrationResult:
    attendee: Attendee
    attendee_registered_event: AttendeeRegisteredEvent
```

[Step 4: Aggregates](04-Aggregates.md)

## Learning Objectives

- Understand how to cleanly package multiple outputs from domain operations
- Implement `AttendeeRegistrationResult` to encapsulate both domain state and events
- Learn how Python handles forward references with `TYPE_CHECKING`

## What We Are Building

An `AttendeeRegistrationResult` frozen dataclass that packages together both the created `Attendee` aggregate and the `AttendeeRegisteredEvent` that needs to be published.

## Why Combining Return Values Matters

When an attendee registers, the operation produces two things: the `Attendee` (the domain state representing the new attendee) and an `AttendeeRegisteredEvent` (a notification for other parts of the system). A Python function can only return one object, so we need a container that holds both outputs together.

You could use a tuple, but tuples communicate nothing about what they contain. Accessing `result[0]` and `result[1]` forces readers to remember which index holds which value. A named dataclass makes the intent explicit: `result.attendee` and `result.attendee_registered_event` are self-documenting.

This pattern appears frequently in DDD. Aggregates often produce both state changes and events in a single operation. A result object keeps them bundled together so the calling service can persist the aggregate and publish the event without any ambiguity about what came back.

## Implementation

Add the following to `conference/attendees/domain/services.py`. The complete file after Steps 2 and 3 should look like this:

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

# TYPE_CHECKING is False at runtime, True during static analysis.
# This avoids circular imports: services.py references Attendee,
# and aggregates.py references AttendeeRegistrationResult.
if TYPE_CHECKING:
    from conference.attendees.domain.aggregates import Attendee

from conference.attendees.domain.events import AttendeeRegisteredEvent


@dataclass(frozen=True)
class RegisterAttendeeCommand:
    """
    Commands encapsulate the intent to perform a business operation.
    Unlike events, commands can fail or be rejected.
    """

    email: str

    def __post_init__(self):
        if not self.email or self.email.strip() == "":
            raise ValueError("Email cannot be null or blank")
        if "@" not in self.email:
            raise ValueError("Email must contain @ symbol")


@dataclass(frozen=True)
class AttendeeRegistrationResult:
    """Packages together the outputs of the registration operation."""

    # The newly created Attendee aggregate
    attendee: Attendee

    # The event to publish, notifying other systems of the registration
    attendee_registered_event: AttendeeRegisteredEvent
```

### Handling the Forward Reference

Notice the `TYPE_CHECKING` guard and `from __future__ import annotations` at the top of the file. The `Attendee` class (which we will build in Step 4) lives in `aggregates.py` and imports `AttendeeRegistrationResult` from this file. If `services.py` also imported `Attendee` at the top level, Python would hit a circular import error at startup.

The solution is a standard Python pattern:

1. `from __future__ import annotations` makes all annotations into strings that are evaluated lazily, so Python does not try to resolve `Attendee` at class-definition time.
2. `TYPE_CHECKING` is `False` at runtime, so the `from conference.attendees.domain.aggregates import Attendee` line never actually executes during normal program execution. It only runs during static analysis (mypy, pyright, IDE type checking).

This keeps type safety intact for tooling while avoiding the circular import at runtime.

**This file will not be independently testable until Step 4**, when we implement the `Attendee` aggregate. That is intentional -- we are building the domain model step by step, and the result object only makes sense once both of its components exist.

## Key Design Decisions

- **Frozen dataclass, not a tuple.** Named fields (`attendee`, `attendee_registered_event`) make the code self-documenting. A tuple would work mechanically but obscures intent.
- **`TYPE_CHECKING` for forward references.** This is the standard Python approach to breaking circular imports while preserving type annotations. It is not a hack -- it is the recommended pattern from PEP 484.
- **Package placement.** The result object lives alongside the service and command in `services.py`, since it is part of the service layer's API contract. It is not a domain concept in its own right -- it is a coordination artifact.

## Testing Your Implementation

The `AttendeeRegistrationResult` is not directly testable at this step because the `Attendee` class does not exist yet. It will be tested indirectly through the `Attendee` aggregate tests in Step 4 and the `AttendeeService` tests in later steps.

After completing Step 4, you can verify the result object works by running:

```bash
pytest tests/domain/test_aggregates.py -v
```

## Next Steps

Now we will implement the `Attendee` aggregate -- the heart of the domain model -- which will use both the event from Step 1 and the result object from this step: [Step 4: Aggregates](04-Aggregates.md)
