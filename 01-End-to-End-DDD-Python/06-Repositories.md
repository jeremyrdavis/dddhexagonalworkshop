# Step 6: Repositories

## tl;dr

_If you want to get the application up and running as quickly as possible you can copy/paste the code into the stubbed classes without reading the rest of the material._

Create `conference/attendees/persistence/repository.py`:

```python
from sqlalchemy.orm import Session

from conference.attendees.domain.aggregates import Attendee
from conference.attendees.persistence.entity import AttendeeEntity


class AttendeeRepository:
    def __init__(self, session: Session):
        self._session = session

    def persist(self, aggregate: Attendee) -> None:
        entity = self._from_aggregate(aggregate)
        self._session.add(entity)
        self._session.flush()

    def _from_aggregate(self, attendee: Attendee) -> AttendeeEntity:
        return AttendeeEntity(email=attendee.email)
```

[Step 7: Outbound Adapters](07-Outbound-Adapters.md)

---

## Concept

A **Repository** represents all objects of a certain type as a conceptual set. It acts like an in-memory collection but is backed by a database. Objects of the appropriate type are added and removed, and the machinery behind the repository inserts them or deletes them from the database.

In DDD, the repository is the bridge between the domain and persistence layers. The domain aggregate (our `Attendee` class) knows nothing about databases. The persistence entity (`AttendeeEntity`) knows nothing about business logic. The repository is what connects them, translating between the two representations.

In the Java version of this workshop, `AttendeeRepository` extends Quarkus's `PanacheRepository<AttendeeEntity>` and uses `@ApplicationScoped` for CDI injection. In Python, we take a simpler approach: we accept a SQLAlchemy `Session` via the constructor and use it directly. There is no framework magic -- just a plain class with explicit dependencies.

## Implementation

Create or update `conference/attendees/persistence/repository.py`:

```python
from sqlalchemy.orm import Session

from conference.attendees.domain.aggregates import Attendee
from conference.attendees.persistence.entity import AttendeeEntity


class AttendeeRepository:
    """
    A REPOSITORY represents all objects of a certain type as a conceptual set.
    It acts like an in-memory collection but is backed by a database.
    -- Eric Evans, Domain-Driven Design, 2003
    """

    def __init__(self, session: Session):
        # The repository receives its database session from the outside.
        # This is constructor injection -- the Python equivalent of
        # @Inject in Java/Quarkus.
        self._session = session

    def persist(self, aggregate: Attendee) -> None:
        """Transform the aggregate to an entity and persist it."""
        # Convert domain aggregate to persistence entity
        entity = self._from_aggregate(aggregate)
        # Add to the SQLAlchemy session (equivalent to entityManager.persist())
        self._session.add(entity)
        # Flush ensures the INSERT is sent to the database immediately,
        # so auto-generated IDs are available. The actual COMMIT happens
        # later in the get_db() dependency (see database.py).
        self._session.flush()

    def _from_aggregate(self, attendee: Attendee) -> AttendeeEntity:
        """Convert a domain aggregate to a persistence entity.

        This is where domain concepts are mapped to database structures.
        The conversion keeps domain and persistence models cleanly separated.
        """
        return AttendeeEntity(email=attendee.email)
```

### Comparing to the Java Version

| Java (Quarkus/Panache)                         | Python (SQLAlchemy)                       |
|------------------------------------------------|-------------------------------------------|
| `extends PanacheRepository<AttendeeEntity>`    | Plain class, no inheritance needed        |
| `@ApplicationScoped`                           | Instantiated per-request via `Depends()`  |
| `@Inject EntityManager`                        | `__init__(self, session: Session)`        |
| `persist(attendeeEntity)` (inherited)          | `self._session.add(entity)`              |
| `entityManager.flush()`                        | `self._session.flush()`                  |
| Transaction managed by `@Transactional` or `QuarkusTransaction` | Transaction managed by `get_db()` context manager |

## Key Design Decisions

- **Aggregate-to-entity conversion lives in the repository.** The `_from_aggregate()` helper method keeps the mapping logic in one place. The domain aggregate never imports SQLAlchemy, and the persistence entity never contains business logic. This is the same pattern as the Java `fromAggregate()` method.

- **The repository uses constructor injection, not global state.** Instead of importing a global session or using a module-level singleton, the `Session` is passed in via `__init__`. This makes the class easy to test with an in-memory SQLite database and keeps the dependency explicit.

- **`flush()` instead of `commit()`.** The repository flushes (sends SQL to the database) but does not commit the transaction. The commit is handled by the `get_db()` dependency in `database.py`, which commits after the entire request succeeds or rolls back on failure. This gives you atomic request-level transactions.

## Testing

Create `tests/persistence/test_repository.py`:

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from conference.attendees.domain.aggregates import Attendee
from conference.attendees.persistence.entity import AttendeeEntity
from conference.attendees.persistence.repository import AttendeeRepository
from database import Base


@pytest.fixture
def session():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestSession = sessionmaker(bind=engine)
    session = TestSession()
    yield session
    session.close()


class TestAttendeeRepository:
    def test_persist_attendee(self, session):
        repo = AttendeeRepository(session=session)
        attendee = Attendee("gandalfthegrey@istari.net")

        repo.persist(attendee)
        session.commit()

        entity = session.query(AttendeeEntity).first()
        assert entity is not None
        assert entity.email == "gandalfthegrey@istari.net"
        assert entity.id is not None
```

Notice how the test uses an in-memory SQLite database (`sqlite:///:memory:`) instead of PostgreSQL. Because the repository only depends on a SQLAlchemy `Session`, we can swap the database engine without changing any application code. This is the power of the repository pattern -- the domain does not care which database is behind the curtain.

## Next Step

In the next section we will create a second outbound adapter, `AttendeeEventPublisher`, to send messages to the rest of the system: [Step 7: Outbound Adapters](07-Outbound-Adapters.md)
