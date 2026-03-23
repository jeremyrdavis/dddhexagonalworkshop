from dataclasses import dataclass


@dataclass(frozen=True)
class AttendeeRegisteredEvent:
    """
    A Domain Event is a record of some business-significant occurrence in a Bounded Context.
    -- Vaughn Vernon, Domain-Driven Design Distilled, 2016

    Events are immutable facts that have already happened. They capture what the business
    cares about and enable loose coupling between system components.

    Note: The event includes full_name but NOT the address. This is a deliberate
    bounded context decision — downstream consumers need to know who registered,
    but the address is internal to the attendee context.
    """

    email: str
    full_name: str
