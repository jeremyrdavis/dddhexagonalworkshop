# Step 4: Aggregates

## TL;DR

Create `conference/attendees/domain/aggregates.py`:

```python
from conference.attendees.domain.events import AttendeeRegisteredEvent
from conference.attendees.domain.services import AttendeeRegistrationResult


class Attendee:
    def __init__(self, email: str):
        self._email = email

    @classmethod
    def register_attendee(cls, email: str) -> AttendeeRegistrationResult:
        attendee = cls(email)
        event = AttendeeRegisteredEvent(email=email)
        return AttendeeRegistrationResult(attendee=attendee, attendee_registered_event=event)

    @property
    def email(self) -> str:
        return self._email
```

[Step 5: Entities](05-Entities.md)

## Learning Objectives

- Understand Aggregates as the core building blocks of Domain-Driven Design
- Implement the `Attendee` aggregate with a factory method and encapsulated state
- Connect Commands, business logic, and Result objects through aggregate methods
- Learn how Python's `@classmethod` and `@property` map to Java's static factory methods and getters

## What We Are Building

An `Attendee` aggregate that encapsulates the business logic for attendee registration and maintains consistency within the attendee bounded context.

## Why Aggregates Are the Heart of DDD

Aggregates solve the most critical problem in business software: where does the business logic live? In many applications, business rules get scattered across controllers, services, and utility classes, making them impossible to find, understand, or change safely. Aggregates solve this by creating a single, authoritative home for all business logic related to a specific business concept.

The `Attendee` aggregate represents a real-world conference attendee and encapsulates all invariants (business rules) associated with that concept. Every business operation flows through the aggregate, every business rule is enforced by the aggregate, and every significant state change originates from the aggregate.

In this iteration, the aggregate is simple -- it holds an email and produces a registration result. But the pattern is what matters. As the system grows, this is where you add rules like "an attendee cannot register twice," "early-bird registration closes on a specific date," or "attendees must have a valid payment method."

## Implementation

Create or update `conference/attendees/domain/aggregates.py`:

```python
from conference.attendees.domain.events import AttendeeRegisteredEvent
from conference.attendees.domain.services import AttendeeRegistrationResult


class Attendee:
    """
    An AGGREGATE is a cluster of associated objects that we treat as a unit
    for the purpose of data changes.
    -- Eric Evans, Domain-Driven Design, 2003

    The Attendee aggregate encapsulates the business logic for attendee
    registration. It uses a factory method to ensure both the aggregate
    and the domain event are created together.
    """

    def __init__(self, email: str):
        # Private attribute -- external code accesses email through the property
        self._email = email

    @classmethod
    def register_attendee(cls, email: str) -> AttendeeRegistrationResult:
        """Factory method that creates an Attendee and its registration event.

        This is a class method rather than a regular constructor because
        registration produces multiple outputs: the aggregate itself and
        a domain event. Returning an AttendeeRegistrationResult bundles
        both together cleanly.
        """
        # Create the aggregate
        attendee = cls(email)

        # Create the domain event recording what happened
        event = AttendeeRegisteredEvent(email=email)

        # Return both, packaged in the result object from Step 3
        return AttendeeRegistrationResult(
            attendee=attendee,
            attendee_registered_event=event,
        )

    @property
    def email(self) -> str:
        """Read-only access to the attendee's email address."""
        return self._email
```

### Python Equivalents for Java Patterns

**Static factory method becomes `@classmethod`.** In Java, `Attendee.registerAttendee()` is a static method. Python's `@classmethod` serves the same purpose: it is called on the class itself (`Attendee.register_attendee("...")`), not on an instance. It also receives `cls` as the first argument, which means subclasses work correctly if you ever need them.

**Private constructor becomes a private attribute with `@property`.** Java uses a `private` constructor to force all creation through the factory method. Python does not have true access control, but by convention, prefixing `_email` with an underscore signals "do not access directly." The `@property` decorator provides read-only access, similar to a Java getter with no setter.

**Aggregate is a plain class, not a dataclass.** Unlike events and commands, the `Attendee` is not a frozen dataclass. Aggregates may need to evolve their state through business operations in future steps (for example, updating contact information). Using a plain class gives us that flexibility.

## Key Design Decisions

- **Factory method, not a plain constructor.** Registration produces two things: the aggregate and an event. A constructor can only return `self`, but a `@classmethod` factory can return an `AttendeeRegistrationResult` containing both. This ensures the aggregate and its event are always created together.
- **Private state with property access.** The `_email` attribute is private by convention. The `@property` provides read-only access, preventing external code from modifying the aggregate's state without going through its business methods.
- **No framework dependencies.** The `Attendee` class is pure Python. It does not import SQLAlchemy, FastAPI, or any other framework. This makes it trivial to unit test and keeps business logic independent of infrastructure choices.

## Testing Your Implementation

Create or update `tests/domain/test_aggregates.py`:

```python
from conference.attendees.domain.aggregates import Attendee
from conference.attendees.domain.events import AttendeeRegisteredEvent
from conference.attendees.domain.services import AttendeeRegistrationResult


class TestAttendee:
    def test_register_attendee_returns_result(self):
        """The factory method should return an AttendeeRegistrationResult."""
        result = Attendee.register_attendee("gandalfthegrey@istari.net")
        assert isinstance(result, AttendeeRegistrationResult)

    def test_register_attendee_creates_aggregate(self):
        """The result should contain an Attendee with the correct email."""
        result = Attendee.register_attendee("gandalfthegrey@istari.net")
        assert result.attendee.email == "gandalfthegrey@istari.net"

    def test_register_attendee_creates_event(self):
        """The result should contain a matching AttendeeRegisteredEvent."""
        result = Attendee.register_attendee("gandalfthegrey@istari.net")
        assert isinstance(result.attendee_registered_event, AttendeeRegisteredEvent)
        assert result.attendee_registered_event.email == "gandalfthegrey@istari.net"
```

Run the tests:

```bash
pytest tests/domain/test_aggregates.py -v
```

All three tests should pass, confirming that the factory method produces both an aggregate and an event, packaged correctly in the result object.

With this step complete, the `AttendeeRegistrationResult` from Step 3 is now fully functional -- you can also go back and verify the earlier tests still pass:

```bash
pytest tests/domain/ -v
```

## Next Steps

In the next step, we will create the `AttendeeEntity` that handles persisting attendee data to the database, separate from the domain aggregate we just built: [Step 5: Entities](05-Entities.md)
