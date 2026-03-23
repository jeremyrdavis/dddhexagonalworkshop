from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from conference.attendees.domain.aggregates import Attendee
    from conference.attendees.infrastructure.dto import AttendeeDTO
    from conference.attendees.infrastructure.event_publisher import AttendeeEventPublisher
    from conference.attendees.persistence.repository import AttendeeRepository

from conference.attendees.domain.events import AttendeeRegisteredEvent

logger = logging.getLogger(__name__)


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

    attendee: Attendee
    attendee_registered_event: AttendeeRegisteredEvent


class AttendeeService:
    """
    Application service that orchestrates the attendee registration workflow.

    The application service coordinates between the domain aggregate, repository,
    and event publisher. It does not contain business logic itself.
    """

    def __init__(
        self,
        repository: AttendeeRepository,
        event_publisher: AttendeeEventPublisher,
    ):
        self._repository = repository
        self._event_publisher = event_publisher

    async def register_attendee(self, command: RegisterAttendeeCommand) -> AttendeeDTO:
        from conference.attendees.domain.aggregates import Attendee
        from conference.attendees.infrastructure.dto import AttendeeDTO

        # Call aggregate factory method
        result = Attendee.register_attendee(command.email)

        # Persist the attendee
        self._repository.persist(result.attendee)

        # Notify the system that a new attendee has been registered
        await self._event_publisher.publish(result.attendee_registered_event)

        return AttendeeDTO(email=result.attendee.email)
