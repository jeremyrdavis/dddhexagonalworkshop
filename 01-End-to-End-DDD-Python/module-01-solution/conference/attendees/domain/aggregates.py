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
        self._email = email

    @classmethod
    def register_attendee(cls, email: str) -> AttendeeRegistrationResult:
        """Factory method that creates an Attendee and its registration event."""
        attendee = cls(email)
        event = AttendeeRegisteredEvent(email=email)
        return AttendeeRegistrationResult(
            attendee=attendee,
            attendee_registered_event=event,
        )

    @property
    def email(self) -> str:
        return self._email
