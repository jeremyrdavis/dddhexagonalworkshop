# Step 4: Update the AttendeeRegisteredEvent

## TL;DR

Update `conference/attendees/domain/events.py`:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class AttendeeRegisteredEvent:
    email: str
    full_name: str
```

[Step 5: Update the Persistence Layer](05-Update-Persistence.md)

## What We Are Building

In this step, we update the `AttendeeRegisteredEvent` to include the attendee's full name. This demonstrates thoughtful event design -- including relevant information while avoiding over-coupling between bounded contexts.

## The Key Design Decision: What NOT to Include

The important thing to note here is that while we have added the attendee's `full_name`, we have **not** added the address to the event. This is a deliberate bounded context decision.

We have decided not to share all of the attendee's information with other Bounded Contexts. If another Bounded Context needs the attendee's address -- for example, if something needs to be mailed to an individual attendee -- we can implement a method that allows other parts of the system to query for the information.

## Implementation

Update `conference/attendees/domain/events.py`:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class AttendeeRegisteredEvent:
    """
    A Domain Event is a record of some business-significant occurrence
    in a Bounded Context.
    -- Vaughn Vernon, Domain-Driven Design Distilled, 2016

    Note: The event includes full_name but NOT the address. This is a deliberate
    bounded context decision -- downstream consumers need to know who registered,
    but the address is internal to the attendee context.
    """

    email: str
    full_name: str
```

## What We Include

- **Email**: Primary identifier for the attendee
- **Full Name**: Useful for notifications and displays in other contexts

## What We Don't Include

- **Address**: Not included because it is sensitive and not necessary for most event subscribers
- **Individual Name Fields**: We provide the computed full name instead of separate first/last

## Strategic Design Considerations

**Bounded Context Integration**: If a different Bounded Context needs an attendee's address in the future, we can work with the team that owns that context to implement a method for them to query our service.

This approach:

- Keeps events lean and focused
- Reduces coupling between bounded contexts
- Allows for future evolution through explicit integration patterns

## Event Design Principles

1. **Minimal Information**: Include only what subscribers actually need
2. **Stable Interface**: Changes to internal models don't break event consumers
3. **Business-Focused**: Events represent business occurrences, not technical changes
4. **Immutable**: Using frozen dataclasses ensures events can't be modified after creation

## Next Step

Continue to [Step 5: Update the Persistence Layer](05-Update-Persistence.md)
