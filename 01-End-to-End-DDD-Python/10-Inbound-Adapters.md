# Step 10: Inbound Adapters

## tl;dr

_If you want to get the application up and running as quickly as possible you can copy/paste the code into the stubbed classes without reading the rest of the material._

Create `conference/attendees/infrastructure/endpoint.py`:

```python
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
    email: str


def get_attendee_service(db: Session = Depends(get_db)) -> AttendeeService:
    repository = AttendeeRepository(session=db)
    event_publisher = AttendeeEventPublisher(producer=None)
    return AttendeeService(repository=repository, event_publisher=event_publisher)


@router.post("/", response_model=AttendeeDTO, status_code=status.HTTP_201_CREATED)
async def register_attendee(
    request: RegisterAttendeeRequest,
    service: AttendeeService = Depends(get_attendee_service),
) -> AttendeeDTO:
    try:
        command = RegisterAttendeeCommand(email=request.email)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))

    attendee_dto = await service.register_attendee(command)
    return attendee_dto
```

---

## Concept

An **inbound adapter** is the entry point where the outside world meets your domain. In our case, it is a REST endpoint that accepts HTTP POST requests, translates them into domain commands, delegates to the application service, and returns the result as an HTTP response. The endpoint knows about HTTP, JSON, and Pydantic. The domain knows about none of those things.

The endpoint performs a critical translation: it converts a **Pydantic request model** (`RegisterAttendeeRequest`) into a **domain command dataclass** (`RegisterAttendeeCommand`). This is the boundary between the HTTP/Pydantic world and the domain/dataclass world. The request model handles JSON deserialization and HTTP-level validation. The domain command handles business validation (is the email non-blank? does it contain an `@`?).

In Java/Quarkus, the inbound adapter is a class annotated with `@Path` and `@POST`, with dependencies injected via `@Inject`. In Python, we use a **FastAPI `APIRouter`** with route decorators and `Depends()` for dependency injection. The mapping is direct: `@Path("/attendees")` becomes `APIRouter(prefix="/attendees")`, `@POST` becomes `@router.post("/")`, and `@Inject` becomes `Depends()`.

## Implementation

Create or update `conference/attendees/infrastructure/endpoint.py`:

```python
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

# Create a router with a URL prefix and OpenAPI tag.
# Java equivalent: @Path("/attendees")
router = APIRouter(prefix="/attendees", tags=["attendees"])


class RegisterAttendeeRequest(BaseModel):
    """Pydantic model for the inbound HTTP request body.

    This is an infrastructure concern -- it defines what the HTTP API
    accepts. It is separate from the domain's RegisterAttendeeCommand.
    """

    email: str


def get_attendee_service(db: Session = Depends(get_db)) -> AttendeeService:
    """Dependency injection: wire repository and event publisher into the service.

    This function is the Python equivalent of Quarkus CDI wiring.
    FastAPI calls it automatically when a route handler declares
    `service: AttendeeService = Depends(get_attendee_service)`.

    The dependency chain: get_db() yields a Session -> AttendeeRepository
    receives that Session -> AttendeeEventPublisher wraps a Kafka producer
    -> AttendeeService receives both collaborators.
    """
    repository = AttendeeRepository(session=db)
    # In production, the producer would be initialized at app startup.
    # For the workshop, we pass None so the publisher logs a warning
    # instead of sending to Kafka (see the None guard in Step 7).
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

    # TRANSLATION BOUNDARY: Convert the Pydantic request model (infrastructure)
    # to a domain command (dataclass). This is where the HTTP world ends
    # and the domain world begins.
    try:
        command = RegisterAttendeeCommand(email=request.email)
    except ValueError as e:
        # The domain command validates business rules (non-blank, contains @).
        # If validation fails, translate the domain ValueError into an
        # HTTP 422 response. The endpoint handles this translation so the
        # domain never needs to know about HTTP status codes.
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e),
        )

    # Delegate to the application service. The service orchestrates
    # aggregate creation, persistence, and event publishing.
    attendee_dto = await service.register_attendee(command)

    logger.debug("Created attendee %s", attendee_dto)

    # FastAPI automatically serializes the Pydantic AttendeeDTO to JSON
    # and returns it with the 201 status code declared above.
    return attendee_dto
```

### Comparing to the Java Version

| Java (JAX-RS / Quarkus)                        | Python (FastAPI)                                |
|------------------------------------------------|------------------------------------------------|
| `@Path("/attendees")`                          | `APIRouter(prefix="/attendees")`               |
| `@POST`                                       | `@router.post("/")`                            |
| `@Consumes(MediaType.APPLICATION_JSON)`        | Automatic (Pydantic request model)             |
| `@Produces(MediaType.APPLICATION_JSON)`        | `response_model=AttendeeDTO`                   |
| `@Inject AttendeeService`                      | `Depends(get_attendee_service)`                |
| JAX-RS auto-deserializes JSON to record        | FastAPI auto-deserializes JSON to Pydantic model |
| Return `Response.status(201).entity(dto).build()` | `status_code=status.HTTP_201_CREATED` + return dto |

### The Translation Pattern

The endpoint makes two translations:

1. **Inbound:** `RegisterAttendeeRequest` (Pydantic) -> `RegisterAttendeeCommand` (dataclass). This crosses the infrastructure/domain boundary.
2. **Outbound:** `AttendeeDTO` (Pydantic) -> JSON HTTP response. FastAPI handles this automatically.

This double translation is the hallmark of hexagonal architecture. The outside world speaks HTTP and JSON. The domain speaks commands and events. The inbound adapter is the translator between these two languages.

### Dependency Injection with `Depends()`

FastAPI's `Depends()` is a function-based dependency injection system. When a route parameter is declared as `service: AttendeeService = Depends(get_attendee_service)`, FastAPI:

1. Calls `get_attendee_service()` before the route handler runs
2. Resolves nested dependencies (`get_db()` is itself a `Depends()`)
3. Passes the constructed service to the handler
4. Cleans up resources after the response is sent (the `get_db()` generator commits and closes the session)

This is simpler than Java CDI but achieves the same result: the endpoint receives fully constructed collaborators without knowing how to build them.

## Key Design Decisions

- **The endpoint translates between Pydantic and dataclass worlds.** The `RegisterAttendeeRequest` is Pydantic (for HTTP deserialization), and the `RegisterAttendeeCommand` is a dataclass (for domain purity). The endpoint manually constructs the command from the request. This one line of translation code is the price of keeping the domain framework-free.

- **Domain validation errors become HTTP errors.** The `try/except ValueError` block translates domain validation failures into `HTTPException` with a 422 status code. The domain raises plain `ValueError` -- it never imports `HTTPException` or knows about status codes. The adapter handles the translation.

- **The dependency function `get_attendee_service()` is the composition root.** This is where all the pieces come together: database session, repository, event publisher, and service. It is the only place in the codebase that knows about all the concrete implementations. Everything else depends on abstractions (constructor parameters).

## Testing

Create `tests/infrastructure/test_endpoint.py`:

```python
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from conference.attendees.infrastructure.endpoint import router
from database import Base, get_db

# Set up an in-memory SQLite database for testing
engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(bind=engine)
TestSession = sessionmaker(bind=engine)


def override_get_db():
    db = TestSession()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# Create a test FastAPI app with the router and overridden dependencies
app = FastAPI()
app.include_router(router)
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestAttendeeEndpoint:
    def test_register_attendee_returns_201(self):
        response = client.post(
            "/attendees/",
            json={"email": "gandalfthegrey@istari.net"},
        )
        assert response.status_code == 201

    def test_register_attendee_returns_email(self):
        response = client.post(
            "/attendees/",
            json={"email": "sarumanthewhite@istari.net"},
        )
        assert response.json()["email"] == "sarumanthewhite@istari.net"

    def test_register_attendee_rejects_invalid_email(self):
        response = client.post(
            "/attendees/",
            json={"email": "notanemail"},
        )
        assert response.status_code == 422
```

The test uses FastAPI's `TestClient` with an in-memory SQLite database. The key technique is `app.dependency_overrides[get_db] = override_get_db`, which swaps the production database session for a test session. This is the same pattern as overriding CDI beans in a Quarkus `@QuarkusTest`.

---

You have now completed all 10 steps of Module 01. The full request flow is:

```
HTTP POST /attendees/ {"email": "..."}
    -> RegisterAttendeeRequest (Pydantic)
    -> RegisterAttendeeCommand (dataclass)
    -> Attendee.register_attendee() (aggregate factory)
    -> AttendeeRepository.persist() (outbound adapter -> DB)
    -> AttendeeEventPublisher.publish() (outbound adapter -> Kafka)
    -> AttendeeDTO (Pydantic)
    -> HTTP 201 {"email": "..."}
```

Every layer speaks its own language, and the adapters translate between them. That is hexagonal architecture in action.
