import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from conference.attendees.domain.services import AttendeeService, RegisterAttendeeCommand
from conference.attendees.domain.valueobjects import Address, MealPreference, TShirtSize
from conference.attendees.infrastructure.dto import AttendeeDTO
from conference.attendees.infrastructure.event_publisher import AttendeeEventPublisher
from conference.attendees.persistence.repository import AttendeeRepository
from database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/attendees", tags=["attendees"])


class AddressRequest(BaseModel):
    """Pydantic model for the address portion of the request body."""

    street_address: str
    bus: str | None = None
    postal_code: str
    town_or_municipality: str


class RegisterAttendeeRequest(BaseModel):
    """Pydantic model for the inbound HTTP request body."""

    email: str
    first_name: str
    last_name: str
    address: AddressRequest
    meal_preference: str
    tshirt_size: str


def get_attendee_service(db: Session = Depends(get_db)) -> AttendeeService:
    """Dependency injection: wire repository and event publisher into the service."""
    repository = AttendeeRepository(session=db)
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

    # Translate Pydantic request models to domain objects
    try:
        address = Address(
            street_address=request.address.street_address,
            bus=request.address.bus,
            postal_code=request.address.postal_code,
            town_or_municipality=request.address.town_or_municipality,
        )
        command = RegisterAttendeeCommand(
            email=request.email,
            first_name=request.first_name,
            last_name=request.last_name,
            address=address,
            meal_preference=MealPreference(request.meal_preference),
            tshirt_size=TShirtSize(request.tshirt_size),
        )
    except (ValueError, KeyError) as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))

    attendee_dto = await service.register_attendee(command)

    logger.debug("Created attendee %s", attendee_dto)
    return attendee_dto
