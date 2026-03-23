# Step 7: Update the Service, Endpoint, and Event Publisher

## TL;DR

This step updates three files. Update `conference/attendees/domain/services.py` (the `AttendeeService.register_attendee` method):

```python
async def register_attendee(self, command: RegisterAttendeeCommand) -> AttendeeDTO:
    from conference.attendees.domain.aggregates import Attendee
    from conference.attendees.infrastructure.dto import AttendeeDTO

    result = Attendee.register_attendee(
        command.email, command.first_name, command.last_name, command.address
    )
    self._repository.persist(result.attendee)
    await self._event_publisher.publish(result.attendee_registered_event)
    return AttendeeDTO(email=result.attendee.email, full_name=result.attendee.full_name)
```

Update `conference/attendees/infrastructure/endpoint.py` to add `AddressRequest` and update the request handling:

```python
from conference.attendees.domain.valueobjects import Address

class AddressRequest(BaseModel):
    street_address: str
    bus: str | None = None
    postal_code: str
    town_or_municipality: str

class RegisterAttendeeRequest(BaseModel):
    email: str
    first_name: str
    last_name: str
    address: AddressRequest
```

Update `conference/attendees/infrastructure/event_publisher.py` to include `full_name`:

```python
value = json.dumps({"email": event.email, "full_name": event.full_name}).encode("utf-8")
```

## Overview

In this final step, we wire everything together. The application service, endpoint, and event publisher all need updates to handle the new fields.

## Step 7.1: Update the AttendeeService

Update the `register_attendee` method in `conference/attendees/domain/services.py`:

```python
async def register_attendee(self, command: RegisterAttendeeCommand) -> AttendeeDTO:
    from conference.attendees.domain.aggregates import Attendee
    from conference.attendees.infrastructure.dto import AttendeeDTO

    # Call aggregate factory method with all fields
    result = Attendee.register_attendee(
        command.email, command.first_name, command.last_name, command.address
    )

    # Persist the attendee
    self._repository.persist(result.attendee)

    # Notify the system that a new attendee has been registered
    await self._event_publisher.publish(result.attendee_registered_event)

    return AttendeeDTO(email=result.attendee.email, full_name=result.attendee.full_name)
```

The service orchestrates the workflow but contains no business logic. It delegates to the aggregate factory method, persists via the repository, publishes the event, and returns a DTO.

## Step 7.2: Update the Endpoint

Update `conference/attendees/infrastructure/endpoint.py` to accept the new request format:

```python
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from conference.attendees.domain.services import AttendeeService, RegisterAttendeeCommand
from conference.attendees.domain.valueobjects import Address
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


def get_attendee_service(db: Session = Depends(get_db)) -> AttendeeService:
    repository = AttendeeRepository(session=db)
    event_publisher = AttendeeEventPublisher(producer=None)
    return AttendeeService(repository=repository, event_publisher=event_publisher)


@router.post("/", response_model=AttendeeDTO, status_code=status.HTTP_201_CREATED)
async def register_attendee(
    request: RegisterAttendeeRequest,
    service: AttendeeService = Depends(get_attendee_service),
) -> AttendeeDTO:
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
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))

    attendee_dto = await service.register_attendee(command)

    logger.debug("Created attendee %s", attendee_dto)
    return attendee_dto
```

### Boundary Translation

Notice the endpoint translates between two worlds:

1. **Pydantic models** (`AddressRequest`, `RegisterAttendeeRequest`) -- these are HTTP concerns, used for JSON parsing and OpenAPI documentation
2. **Domain objects** (`Address`, `RegisterAttendeeCommand`) -- these are pure domain dataclasses with business validation

The `try/except ValueError` block catches validation errors from the domain objects (e.g., blank street address) and translates them to HTTP 422 responses.

## Step 7.3: Update the Event Publisher

Update `conference/attendees/infrastructure/event_publisher.py` to include `full_name` in the Kafka JSON:

```python
async def publish(self, event: AttendeeRegisteredEvent) -> None:
    if self._producer is None:
        logger.warning("No Kafka producer configured; skipping event publish for %s", event.email)
        return
    value = json.dumps({"email": event.email, "full_name": event.full_name}).encode("utf-8")
    await self._producer.send_and_wait(self._topic, value=value)
    logger.info("Published AttendeeRegisteredEvent for %s", event.email)
```

## Verify Your Work

Run the full test suite:

```bash
pytest -v
```

All tests should pass. You can also start the application and test with curl:

```bash
uvicorn main:app --reload

curl -X POST http://localhost:8000/attendees/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "gandalfthegrey@istari.net",
    "first_name": "Gandalf",
    "last_name": "Grey",
    "address": {
      "street_address": "1 Bag End",
      "postal_code": "12345",
      "town_or_municipality": "Hobbiton"
    }
  }'
```

Expected response (HTTP 201):

```json
{"email": "gandalfthegrey@istari.net", "full_name": "Gandalf Grey"}
```

## Summary

In this module you learned:

- **Value Objects** describe attributes without identity (`Address`)
- **Frozen dataclasses** enforce immutability and value equality
- **Object-relational impedance mismatch** means domain value objects need different persistence strategies
- **Information hiding** across bounded contexts -- events and DTOs include `full_name` but not the address
- How to evolve commands, aggregates, events, and persistence together when adding new domain concepts
