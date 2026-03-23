# Step 3: Inbound Adapter

## TL;DR

Create `conference/attendees/integration/salesteam/endpoint.py`:

```python
import logging
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from conference.attendees.domain.services import AttendeeService
from conference.attendees.infrastructure.event_publisher import AttendeeEventPublisher
from conference.attendees.integration.salesteam.models import SalesteamRegistrationRequest
from conference.attendees.integration.salesteam.translator import SalesteamToDomainTranslator
from conference.attendees.persistence.repository import AttendeeRepository
from database import get_db

logger = logging.getLogger(__name__)
salesteam_router = APIRouter(prefix="/salesteam", tags=["salesteam"])


def get_attendee_service(db: Session = Depends(get_db)) -> AttendeeService:
    repository = AttendeeRepository(session=db)
    event_publisher = AttendeeEventPublisher(producer=None)
    return AttendeeService(repository=repository, event_publisher=event_publisher)


@salesteam_router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def register_from_salesteam(
    request: SalesteamRegistrationRequest,
    service: AttendeeService = Depends(get_attendee_service),
) -> dict:
    commands = SalesteamToDomainTranslator.translate(request.customers)
    for command in commands:
        await service.register_attendee(command)
    return {"registered": len(commands)}
```

Then add to `main.py`:

```python
from conference.attendees.integration.salesteam.endpoint import salesteam_router
app.include_router(salesteam_router)
```

[Step 4: Value Objects](04-Value-Objects.md)

## Overview

The Salesteam endpoint is a separate inbound adapter specifically for the external system. It accepts Salesteam's JSON format, runs it through the translator, and delegates to the existing domain service.

## Key Design Points

### HTTP 202 Accepted (not 201 Created)

The Salesteam endpoint returns 202 instead of 201. This is intentional -- the request represents a bulk operation that has been accepted for processing. The individual attendees are created by the domain service.

### Separate Router

The Salesteam endpoint gets its own FastAPI `APIRouter` with the `/salesteam/` prefix. This keeps it separate from the main `/attendees/` endpoint and makes it clear that this is an integration concern, not a primary domain endpoint.

### Same Domain Service

Both endpoints use the same `AttendeeService`. The integration endpoint translates and then calls the same service method as the main endpoint. This ensures consistent business rules regardless of the registration source.

## Request Flow

```
POST /salesteam/
    |
    v
SalesteamRegistrationRequest (Pydantic parses JSON)
    |
    v
SalesteamToDomainTranslator.translate() (ACL)
    |
    v
List[RegisterAttendeeCommand] (domain commands)
    |
    v
AttendeeService.register_attendee() (for each command)
    |
    v
{"registered": N} (HTTP 202)
```

## Next Step

Continue to [Step 4: Value Objects](04-Value-Objects.md)
