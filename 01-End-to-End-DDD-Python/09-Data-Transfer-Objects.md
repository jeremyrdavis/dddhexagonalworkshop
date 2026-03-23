# Step 9: Data Transfer Objects

## tl;dr

_If you want to get the application up and running as quickly as possible you can copy/paste the code into the stubbed classes without reading the rest of the material._

Create `conference/attendees/infrastructure/dto.py`:

```python
from pydantic import BaseModel


class AttendeeDTO(BaseModel):
    email: str
```

[Step 10: Inbound Adapters](10-Inbound-Adapters.md)

---

## Concept

A **Data Transfer Object (DTO)** defines the data contract between your API and its consumers. DTOs are not specifically a DDD concept -- they come from the broader enterprise patterns world. Their job is to carry data across boundaries (in our case, from the application service to the HTTP response) without exposing internal domain details.

In the Java version, DTOs are implemented as Java records -- lightweight immutable data carriers that the framework automatically serializes to JSON. In Python, we use **Pydantic BaseModel** for DTOs. Pydantic gives us automatic JSON serialization, request/response validation, and seamless integration with FastAPI's OpenAPI documentation. A Pydantic model declared as a FastAPI response type is automatically converted to a JSON response body.

This is where the **domain/infrastructure boundary** becomes visible in the code. Domain objects (`AttendeeRegisteredEvent`, `RegisterAttendeeCommand`, `AttendeeRegistrationResult`) are plain Python dataclasses -- they have no framework dependencies. Infrastructure objects (`AttendeeDTO`, and the `RegisterAttendeeRequest` we will see in Step 10) are Pydantic models -- they depend on Pydantic and exist specifically to serve the HTTP layer. This split is intentional: the domain remains portable and testable, while the infrastructure layer handles serialization concerns.

## Implementation

Create or update `conference/attendees/infrastructure/dto.py`:

```python
from pydantic import BaseModel


class AttendeeDTO(BaseModel):
    """
    Data Transfer Object for Attendee responses.

    DTOs are not specifically a DDD concept. They define the data contract
    between the API and its consumers, separate from the domain model.
    """

    # The email field is automatically validated as a string by Pydantic.
    # When FastAPI returns this model, it is serialized to JSON:
    # {"email": "gandalfthegrey@istari.net"}
    email: str
```

### Why Pydantic for DTOs but Dataclasses for Domain Objects?

This design choice reflects the hexagonal architecture boundary:

| Concern            | Domain Layer              | Infrastructure Layer          |
|--------------------|---------------------------|-------------------------------|
| **Library**        | `dataclasses` (stdlib)    | `pydantic.BaseModel`          |
| **Purpose**        | Model business concepts   | Define API contracts          |
| **Dependencies**   | None (pure Python)        | Pydantic, FastAPI             |
| **Serialization**  | Not their job             | Automatic JSON via FastAPI    |
| **Validation**     | Business rules in code    | Schema validation by Pydantic |
| **Examples**       | `AttendeeRegisteredEvent`, `RegisterAttendeeCommand` | `AttendeeDTO`, `RegisterAttendeeRequest` |

If we used Pydantic in the domain layer, our business logic would depend on an external library. If the Pydantic API changed or we switched web frameworks, we would need to modify domain code. By keeping the domain on plain dataclasses, it remains framework-independent.

### Comparing to the Java Version

| Java                                  | Python                                |
|---------------------------------------|---------------------------------------|
| `public record AttendeeDTO(String email) {}` | `class AttendeeDTO(BaseModel): email: str` |
| Automatic JSON via JAX-RS             | Automatic JSON via FastAPI + Pydantic |
| Immutable by default (record)         | Immutable by default (BaseModel)      |
| No validation annotations needed      | Pydantic validates types at runtime   |

Java records and Pydantic models serve the same purpose: they are simple, immutable data carriers that the framework knows how to serialize. The main difference is that Pydantic also performs runtime type validation, which Java records do not (unless you add Bean Validation annotations).

## Key Design Decisions

- **DTOs live in `infrastructure/`, not `domain/`.** This placement signals that DTOs are an infrastructure concern tied to the HTTP API. The domain layer does not know or care about DTOs. The application service creates the DTO as its final step, translating from the domain world to the API world.

- **Pydantic for infrastructure, dataclasses for domain.** This is the single most visible boundary in the codebase. If you see a `BaseModel`, you know you are in infrastructure. If you see a `@dataclass`, you know you are in the domain. This convention makes the architecture self-documenting.

- **The DTO mirrors the domain model but is not the domain model.** Right now, `AttendeeDTO` looks identical to the domain's email field. As the system grows, the DTO may diverge -- perhaps including a registration timestamp for the API consumer but not exposing internal aggregate state. The separation gives you the freedom to evolve the API contract independently of the domain model.

## Testing

DTOs backed by Pydantic are straightforward to test:

```python
import json

from conference.attendees.infrastructure.dto import AttendeeDTO


class TestAttendeeDTO:
    def test_dto_creation(self):
        dto = AttendeeDTO(email="gandalfthegrey@istari.net")
        assert dto.email == "gandalfthegrey@istari.net"

    def test_dto_serializes_to_json(self):
        dto = AttendeeDTO(email="gandalfthegrey@istari.net")
        data = json.loads(dto.model_dump_json())
        assert data == {"email": "gandalfthegrey@istari.net"}

    def test_dto_from_dict(self):
        dto = AttendeeDTO.model_validate({"email": "gandalfthegrey@istari.net"})
        assert dto.email == "gandalfthegrey@istari.net"
```

These tests verify that the DTO can be created, serialized to JSON, and deserialized from a dictionary -- the three operations FastAPI performs automatically during request handling.

## Next Step

We now have all the building blocks: events, commands, aggregates, entities, repositories, outbound adapters, services, and DTOs. In the final step, we will wire everything together with a REST endpoint: [Step 10: Inbound Adapters](10-Inbound-Adapters.md)
