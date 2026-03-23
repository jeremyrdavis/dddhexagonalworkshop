import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from conference.attendees.domain.services import AttendeeService, RegisterAttendeeCommand
from conference.attendees.infrastructure.dto import AttendeeDTO
from conference.attendees.infrastructure.event_publisher import AttendeeEventPublisher
from conference.attendees.persistence.repository import AttendeeRepository
from database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/attendees", tags=["attendees"])


class RegisterAttendeeRequest(BaseModel):
    """Pydantic model for the inbound HTTP request body."""

    email: str


def get_attendee_service(db: Session = Depends(get_db)) -> AttendeeService:
    """Dependency injection: wire repository and event publisher into the service."""
    repository = AttendeeRepository(session=db)
    # In production, the producer would be initialized at app startup.
    # For the workshop, we use a placeholder that will be wired in a later step.
    event_publisher = AttendeeEventPublisher(producer=None)
    return AttendeeService(repository=repository, event_publisher=event_publisher)


@router.post("/", response_model=AttendeeDTO, status_code=status.HTTP_201_CREATED)
async def register_attendee(
    request: RegisterAttendeeRequest,
    service: AttendeeService = Depends(get_attendee_service),
) -> AttendeeDTO:
    """
    Inbound adapter: translates an HTTP POST request into a domain command,
    delegates to the application service, and returns the result as a DTO.
    """
    logger.debug("Creating attendee %s", request)

    # Translate the Pydantic request model to a domain command
    try:
        command = RegisterAttendeeCommand(email=request.email)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))

    attendee_dto = await service.register_attendee(command)

    logger.debug("Created attendee %s", attendee_dto)
    return attendee_dto
