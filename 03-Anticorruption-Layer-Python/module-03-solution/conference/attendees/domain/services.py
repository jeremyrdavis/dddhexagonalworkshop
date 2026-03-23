from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from conference.attendees.domain.aggregates import Attendee
    from conference.attendees.domain.valueobjects import Address, MealPreference, TShirtSize
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
    first_name: str
    last_name: str
    address: Address | None
    meal_preference: MealPreference
    tshirt_size: TShirtSize

    def __post_init__(self):
        if not self.email or self.email.strip() == "":
            raise ValueError("Email cannot be null or blank")
        if "@" not in self.email:
            raise ValueError("Email must contain @ symbol")
        if not self.first_name or self.first_name.strip() == "":
            raise ValueError("First name cannot be null or blank")
        if not self.last_name or self.last_name.strip() == "":
            raise ValueError("Last name cannot be null or blank")


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

        # Call aggregate factory method (meal_preference and tshirt_size are not passed
        # to the aggregate — they are command-level data only in this iteration)
        result = Attendee.register_attendee(
            command.email, command.first_name, command.last_name, command.address
        )

        # Persist the attendee
        self._repository.persist(result.attendee)

        # Notify the system that a new attendee has been registered
        await self._event_publisher.publish(result.attendee_registered_event)

        return AttendeeDTO(email=result.attendee.email, full_name=result.attendee.full_name)
