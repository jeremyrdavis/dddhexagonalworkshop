from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from conference.attendees.domain.aggregates import Attendee

from conference.attendees.domain.events import AttendeeRegisteredEvent


@dataclass(frozen=True)
class RegisterAttendeeCommand:
    """
    Commands encapsulate the intent to perform a business operation.
    Unlike events, commands can fail or be rejected.
    """

    pass  # TODO: Add the email field and __post_init__ validation


@dataclass(frozen=True)
class AttendeeRegistrationResult:
    """Packages together the outputs of the registration operation."""

    pass  # TODO: Add attendee and attendee_registered_event fields


class AttendeeService:
    """
    Application service that orchestrates the attendee registration workflow.

    The application service coordinates between the domain aggregate, repository,
    and event publisher. It does not contain business logic itself.
    """

    pass  # TODO: Add __init__ and register_attendee method
