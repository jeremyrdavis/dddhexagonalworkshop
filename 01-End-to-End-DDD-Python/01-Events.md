# Step 1: Events

## TL;DR

Add the `AttendeeRegisteredEvent` to `conference/attendees/domain/events.py`:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class AttendeeRegisteredEvent:
    email: str
```

[Step 2: Commands](02-Commands.md)

## Learning Objectives

- Understand the role of Domain Events in capturing business-significant occurrences
- Implement an `AttendeeRegisteredEvent` using Python's frozen dataclasses
- Verify immutability with pytest

## What We Are Building

An `AttendeeRegisteredEvent` dataclass that captures the fact that an attendee has successfully registered for the conference.

## Why Domain Events Matter

Domain Events are immutable statements of fact that the business cares about. They represent things that have already happened -- you cannot undo or reject an event, because it records history. When an attendee registers, that registration is a fact, and multiple parts of the system may need to react: sending a welcome email, updating conference capacity, notifying a billing system, or generating a badge.

By publishing an event like `AttendeeRegisteredEvent`, we enable different components to react independently without tight coupling. The registration code does not need to know about emails, badges, or billing. It simply states "this happened" and moves on.

Events also create a natural audit trail. Because they are immutable records of what occurred, they are valuable for debugging, compliance, and business analytics.

## Implementation

A Domain Event is a record of some business-significant occurrence in a Bounded Context. It is obviously significant that an attendee has registered -- that is how conferences make money -- but it is also significant because other parts of the system need to respond.

For this iteration, we use a minimal event with only the attendee's email address. Create or update `conference/attendees/domain/events.py`:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class AttendeeRegisteredEvent:
    """
    A Domain Event is a record of some business-significant occurrence
    in a Bounded Context.
    -- Vaughn Vernon, Domain-Driven Design Distilled, 2016

    Events are immutable facts that have already happened. They capture
    what the business cares about and enable loose coupling between
    system components.
    """

    # The email of the attendee who registered
    email: str
```

### Why `@dataclass(frozen=True)`?

In the Java version of this workshop, events are modeled as **records** -- a language feature introduced in Java 16 that provides immutable data carriers with automatic `equals()`, `hashCode()`, and `toString()`.

Python's closest equivalent is the **frozen dataclass**. When you pass `frozen=True` to the `@dataclass` decorator:

- All fields become read-only. Attempting to assign a new value raises `FrozenInstanceError`.
- `__eq__` and `__hash__` are generated automatically, so two events with the same data are considered equal.
- The class remains concise and focused on data rather than behavior.

This makes frozen dataclasses a natural fit for Domain Events, which should never be modified after creation.

## Key Design Decisions

- **Why frozen?** Events represent facts that have already happened. They must be immutable. The `frozen=True` parameter enforces this at runtime, raising `FrozenInstanceError` if any code attempts to modify an event after creation.
- **Why only email?** In this iteration we are keeping it simple. In real systems, you might also include a timestamp, an attendee ID, a conference ID, or a registration type (early bird, regular, etc.).
- **Why a dataclass instead of a plain class?** Dataclasses eliminate boilerplate for `__init__`, `__repr__`, `__eq__`, and `__hash__`. This keeps the focus on the domain concept rather than Python plumbing.

## Testing Your Implementation

Create or update `tests/domain/test_events.py` with the following pytest tests:

```python
import dataclasses

import pytest

from conference.attendees.domain.events import AttendeeRegisteredEvent


class TestAttendeeRegisteredEvent:
    def test_event_contains_email(self):
        """An event should store the email it was created with."""
        event = AttendeeRegisteredEvent(email="gandalfthegrey@istari.net")
        assert event.email == "gandalfthegrey@istari.net"

    def test_event_is_immutable(self):
        """Events are facts -- they must not be changed after creation."""
        event = AttendeeRegisteredEvent(email="gandalfthegrey@istari.net")
        with pytest.raises(dataclasses.FrozenInstanceError):
            event.email = "sarumanthewhite@istari.net"

    def test_event_equality(self):
        """Two events with the same data should be considered equal."""
        event1 = AttendeeRegisteredEvent(email="gandalfthegrey@istari.net")
        event2 = AttendeeRegisteredEvent(email="gandalfthegrey@istari.net")
        assert event1 == event2
```

Run the tests from the module directory:

```bash
pytest tests/domain/test_events.py -v
```

All three tests should pass, confirming that the event stores its data, is immutable, and supports value equality.

## Next Steps

Next up is implementing a Command to trigger the registration workflow: [Step 2: Commands](02-Commands.md)
