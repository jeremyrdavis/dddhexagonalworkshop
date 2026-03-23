# Step 8: Application Services

## tl;dr

_If you want to get the application up and running as quickly as possible you can copy/paste the code into the stubbed classes without reading the rest of the material._

Add the `AttendeeService` class to `conference/attendees/domain/services.py` (the `RegisterAttendeeCommand` and `AttendeeRegistrationResult` should already exist from earlier steps):

```python
class AttendeeService:
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

        result = Attendee.register_attendee(command.email)
        self._repository.persist(result.attendee)
        await self._event_publisher.publish(result.attendee_registered_event)
        return AttendeeDTO(email=result.attendee.email)
```

The complete `conference/attendees/domain/services.py` file:

```python
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
    email: str

    def __post_init__(self):
        if not self.email or self.email.strip() == "":
            raise ValueError("Email cannot be null or blank")
        if "@" not in self.email:
            raise ValueError("Email must contain @ symbol")


@dataclass(frozen=True)
class AttendeeRegistrationResult:
    attendee: Attendee
    attendee_registered_event: AttendeeRegisteredEvent


class AttendeeService:
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

        result = Attendee.register_attendee(command.email)
        self._repository.persist(result.attendee)
        await self._event_publisher.publish(result.attendee_registered_event)
        return AttendeeDTO(email=result.attendee.email)
```

[Step 9: Data Transfer Objects](09-Data-Transfer-Objects.md)

---

## Concept

An **application service** orchestrates a business workflow. It coordinates the domain aggregate, repository, and event publisher to accomplish a use case -- but it does not contain business logic itself. The business rules live in the aggregate; the service just calls the right things in the right order.

Think of the application service as a movie director. The director does not act, operate the camera, or compose the music. The director tells the actors when to perform, the camera operator where to point, and the sound engineer when to play the score. Similarly, `AttendeeService.register_attendee()` calls the aggregate factory method, tells the repository to persist, tells the event publisher to publish, and returns a DTO. The service is pure orchestration.

In Java/Quarkus, the application service is annotated with `@ApplicationScoped` and its dependencies are injected via `@Inject`. In Python, we use plain constructor injection -- the repository and event publisher are passed as `__init__` parameters. FastAPI's `Depends()` mechanism handles the wiring at request time, as we will see in Step 10.

## Implementation

Update `conference/attendees/domain/services.py` to include the `AttendeeService`:

```python
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

# TYPE_CHECKING block: these imports are only used for type hints.
# At runtime, Python skips them entirely, which avoids circular imports
# between the domain, infrastructure, and persistence layers.
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
        # Constructor injection: the Python equivalent of
        # @Inject AttendeeRepository and @Inject AttendeeEventPublisher
        self._repository = repository
        self._event_publisher = event_publisher

    async def register_attendee(self, command: RegisterAttendeeCommand) -> AttendeeDTO:
        # Local imports to avoid circular dependencies at module load time.
        # The TYPE_CHECKING block handles type hints; these handle runtime.
        from conference.attendees.domain.aggregates import Attendee
        from conference.attendees.infrastructure.dto import AttendeeDTO

        # Step 1: Call the aggregate factory method.
        # The business logic (creating the attendee and its event) lives
        # entirely inside the Attendee aggregate.
        result = Attendee.register_attendee(command.email)

        # Step 2: Persist the attendee via the repository.
        # The repository handles the aggregate-to-entity conversion.
        self._repository.persist(result.attendee)

        # Step 3: Notify the system that a new attendee has been registered.
        # The event publisher handles Kafka serialization and delivery.
        await self._event_publisher.publish(result.attendee_registered_event)

        # Step 4: Return a DTO for the HTTP response.
        return AttendeeDTO(email=result.attendee.email)
```

### Comparing to the Java Version

| Java (Quarkus)                                        | Python                                              |
|-------------------------------------------------------|-----------------------------------------------------|
| `@ApplicationScoped`                                  | Plain class, no decorator needed                    |
| `@Inject AttendeeRepository`                          | `__init__(self, repository: AttendeeRepository)`    |
| `@Inject AttendeeEventPublisher`                      | `__init__(self, ..., event_publisher: ...)`          |
| `QuarkusTransaction.requiringNew().run(() -> ...)`    | Transaction managed by `get_db()` in `database.py` |
| Synchronous method                                    | `async` method (because event publisher is async)   |

### The Orchestration Pattern

Notice that `register_attendee` follows a strict sequence:

1. **Create** -- call the aggregate factory method
2. **Persist** -- save to the database via the repository
3. **Publish** -- send the domain event via the outbound adapter
4. **Return** -- build and return the DTO

The service does not validate the email (the command does that), does not create the event (the aggregate does that), does not convert to an entity (the repository does that), and does not serialize to JSON (the event publisher does that). Each collaborator has exactly one responsibility.

## Key Design Decisions

- **The service contains zero business logic.** If you find yourself writing `if`/`else` branches or validation rules in the service, that logic probably belongs in the aggregate or the command. The service is strictly a workflow coordinator.

- **The method is `async` because of Kafka.** Even though the repository call is synchronous, the event publisher uses `await` for Kafka I/O. In Python, once any step in the chain is async, the calling method must also be async. This propagates cleanly through FastAPI, which natively handles async endpoints.

- **`TYPE_CHECKING` avoids circular imports.** The services module needs type references to classes from infrastructure and persistence, but those modules may also reference domain types. The `TYPE_CHECKING` guard ensures these imports only exist for type checkers (mypy, IDE autocomplete) and not at runtime.

## Testing

Create `tests/domain/test_services.py`:

```python
from unittest.mock import AsyncMock, MagicMock

import pytest

from conference.attendees.domain.services import AttendeeService, RegisterAttendeeCommand
from conference.attendees.infrastructure.dto import AttendeeDTO


class TestAttendeeService:
    @pytest.fixture
    def mock_repository(self):
        return MagicMock()

    @pytest.fixture
    def mock_event_publisher(self):
        publisher = MagicMock()
        publisher.publish = AsyncMock()
        return publisher

    @pytest.fixture
    def service(self, mock_repository, mock_event_publisher):
        return AttendeeService(
            repository=mock_repository,
            event_publisher=mock_event_publisher,
        )

    @pytest.mark.asyncio
    async def test_register_attendee_persists(self, service, mock_repository):
        command = RegisterAttendeeCommand(email="gandalfthegrey@istari.net")
        await service.register_attendee(command)
        mock_repository.persist.assert_called_once()

    @pytest.mark.asyncio
    async def test_register_attendee_publishes_event(self, service, mock_event_publisher):
        command = RegisterAttendeeCommand(email="gandalfthegrey@istari.net")
        await service.register_attendee(command)
        mock_event_publisher.publish.assert_called_once()

    @pytest.mark.asyncio
    async def test_register_attendee_returns_dto(self, service):
        command = RegisterAttendeeCommand(email="gandalfthegrey@istari.net")
        result = await service.register_attendee(command)
        assert isinstance(result, AttendeeDTO)
        assert result.email == "gandalfthegrey@istari.net"
```

The tests use `MagicMock` for the repository (synchronous) and `AsyncMock` for the event publisher (asynchronous). This verifies that all three steps of the workflow are called without needing a real database or Kafka broker. Each test checks one responsibility: persisting, publishing, or returning the correct DTO.

## Next Step

The service returns an `AttendeeDTO` -- but we have not defined that class yet. Next we will create the Data Transfer Object using Pydantic: [Step 9: Data Transfer Objects](09-Data-Transfer-Objects.md)
