# Step 5: Entities

In Domain-Driven Design, all persistence is handled by repositories, but before we create the repository, we need a persistence entity. Entities represent specific instances of domain objects with database identities.

## TL;DR

Create `conference/attendees/persistence/entity.py`:

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class AttendeeEntity(Base):
    __tablename__ = "attendee"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    def __init__(self, email: str):
        self.email = email

    def __repr__(self) -> str:
        return f"AttendeeEntity(id={self.id}, email='{self.email}')"
```

[Step 6: Repositories](06-Repositories.md)

## Learning Objectives

- Understand the difference between Domain Aggregates and Persistence Entities
- Implement `AttendeeEntity` for database persistence using SQLAlchemy
- Apply the separation between domain logic and persistence concerns
- Learn how SQLAlchemy's `DeclarativeBase` and `mapped_column` map to JPA's `@Entity` and `@Column`

## What We Are Building

An `AttendeeEntity` SQLAlchemy model that represents how attendee data is stored in the database, completely separate from the domain logic in the `Attendee` aggregate.

## Why Entities Are Separate from Aggregates

This is one of the most important architectural decisions in hexagonal architecture: the domain model and the persistence model are different things with different responsibilities. Your `Attendee` aggregate encapsulates business rules. Your `AttendeeEntity` maps data to database columns. Mixing these concerns creates code that is hard to test, hard to change, and tightly coupled to your database technology.

Consider what happens when they are mixed: adding a JPA annotation (or SQLAlchemy column definition) to your domain aggregate means your business logic now depends on your persistence framework. Changing your database schema forces you to touch business logic files. Unit-testing business rules requires a database connection. None of these are desirable.

With clean separation, your domain aggregate is pure Python with no framework dependencies. You can unit-test it instantly. You can change your database from PostgreSQL to MongoDB without touching a single line of business logic. And your persistence entity can be optimized for database performance without compromising domain model clarity.

## Implementation

First, ensure you have a `database.py` module at the project root that defines the SQLAlchemy `Base` class:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
```

Then create or update `conference/attendees/persistence/entity.py`:

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class AttendeeEntity(Base):
    """
    Persistence entity for Attendee data. Separate from the domain aggregate.

    The entity handles database mapping concerns while the aggregate handles
    business logic. This separation is a key principle of Hexagonal Architecture.
    """

    # Map this class to the "attendee" table
    __tablename__ = "attendee"

    # Database primary key -- technical identity for persistence.
    # This is different from business identity (email) in the domain model.
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Business data mapped to a database column.
    # nullable=False and unique=True enforce database-level constraints.
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    def __init__(self, email: str):
        self.email = email

    def __repr__(self) -> str:
        return f"AttendeeEntity(id={self.id}, email='{self.email}')"
```

### Java to Python: Persistence Mapping

| Java (JPA)                                    | Python (SQLAlchemy)                              |
|-----------------------------------------------|--------------------------------------------------|
| `@Entity`                                     | Inherit from `DeclarativeBase` subclass (`Base`) |
| `@Table(name = "attendee")`                   | `__tablename__ = "attendee"`                     |
| `@Id @GeneratedValue(strategy = IDENTITY)`    | `mapped_column(primary_key=True, autoincrement=True)` |
| `@Column(name="email", nullable=false, unique=true)` | `mapped_column(String, nullable=False, unique=True)` |
| `protected AttendeeEntity() {}` (JPA no-arg)  | Not needed -- SQLAlchemy does not require a no-arg constructor |
| `Long id` / `String email` field types        | `Mapped[int]` / `Mapped[str]` type annotations   |

SQLAlchemy's modern `Mapped` type annotations (introduced in SQLAlchemy 2.0) provide type safety similar to what JPA achieves with annotations, but with a more Pythonic feel. The `mapped_column()` function replaces the older `Column()` approach and integrates with Python's type system.

### Entities vs Aggregates: Different Concerns

| Aspect       | Domain Aggregate (`Attendee`)    | Persistence Entity (`AttendeeEntity`) |
|--------------|----------------------------------|---------------------------------------|
| **Purpose**  | Business logic and rules         | Data storage mapping                  |
| **Dependencies** | Pure Python, no frameworks   | SQLAlchemy                            |
| **Identity** | Business identity (email)        | Technical identity (database ID)      |
| **Lifecycle**| Created by business operations   | Created/loaded by ORM                 |
| **Testing**  | Unit tests, no database needed   | Integration tests with database       |

## Key Design Decisions

- **No business logic in the entity.** The entity contains no validation or business rules. That is the aggregate's responsibility. The entity is a data container for the persistence layer, nothing more.
- **Separate identity model.** The entity has an auto-incrementing `id` for database purposes. The domain aggregate uses `email` as its business identity. These serve different purposes and should not be conflated.
- **`__repr__` for debugging.** A readable string representation makes debugging database issues much easier. This is a persistence convenience, not a domain concern.

## Testing Your Implementation

The `AttendeeEntity` is not tested in isolation. It will be tested through the repository integration tests in Step 6, which verify that entities can be persisted to and retrieved from the database.

After completing Step 6, you can run:

```bash
pytest tests/persistence/test_repository.py -v
```

If you want to verify that the entity class is at least importable and structurally correct right now, you can do a quick smoke check:

```bash
python -c "from conference.attendees.persistence.entity import AttendeeEntity; print('Entity class loaded successfully')"
```

## Next Steps

In the next step, we will create the `AttendeeRepository` that bridges between our domain aggregates and these persistence entities. The repository will handle converting `Attendee` aggregates to `AttendeeEntity` objects for storage, and vice versa for retrieval, maintaining the clean separation between domain and persistence concerns: [Step 6: Repositories](06-Repositories.md)
