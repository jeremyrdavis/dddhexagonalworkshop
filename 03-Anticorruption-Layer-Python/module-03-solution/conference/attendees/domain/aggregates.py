from conference.attendees.domain.events import AttendeeRegisteredEvent
from conference.attendees.domain.services import AttendeeRegistrationResult
from conference.attendees.domain.valueobjects import Address


class Attendee:
    """
    An AGGREGATE is a cluster of associated objects that we treat as a unit
    for the purpose of data changes.
    -- Eric Evans, Domain-Driven Design, 2003

    The Attendee aggregate encapsulates the business logic for attendee
    registration. It uses a factory method to ensure both the aggregate
    and the domain event are created together.
    """

    def __init__(self, email: str, first_name: str, last_name: str, address: Address | None):
        self._email = email
        self._first_name = first_name
        self._last_name = last_name
        self._address = address

    @classmethod
    def register_attendee(
        cls, email: str, first_name: str, last_name: str, address: Address | None
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
    def address(self) -> Address | None:
        return self._address

    @property
    def full_name(self) -> str:
        return f"{self._first_name} {self._last_name}"
