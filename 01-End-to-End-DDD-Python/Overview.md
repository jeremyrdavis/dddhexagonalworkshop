# Module 01: End-to-End DDD (Python)

## What You Will Build

In this module you will build a **conference attendee registration system** using Domain-Driven Design and Hexagonal Architecture. By the end you will have a working REST API that accepts registration requests, applies business rules, persists attendees to a database, and publishes domain events to Kafka.

The module walks through the complete DDD workflow in 10 steps, each introducing one building block of the architecture.

## Architecture

The system follows the Hexagonal Architecture (Ports and Adapters) pattern:

```
External World       Inbound Adapter       Domain Layer         Outbound Adapters      External Systems
     |                    |                     |                     |                      |
HTTP POST           FastAPI Router         Attendee             AttendeeRepository        PostgreSQL
/attendees/     ->  endpoint.py        ->  Aggregate        ->  repository.py         ->  Database
                                           aggregates.py
                                                                AttendeeEventPublisher    Kafka
                                                            ->  event_publisher.py    ->  Topic
```

Request flow:

1. An HTTP POST arrives at the FastAPI endpoint (inbound adapter)
2. The endpoint translates the Pydantic request into a domain command (dataclass)
3. The application service calls the aggregate factory method
4. The aggregate creates both the attendee and a domain event
5. The repository persists the attendee to PostgreSQL (outbound adapter)
6. The event publisher sends the event to Kafka (outbound adapter)
7. The service returns a DTO, which FastAPI serializes to JSON

## Technology Stack

| Concern                | Java (Original Workshop)        | Python (This Port)                |
|------------------------|---------------------------------|-----------------------------------|
| Web framework          | Quarkus / JAX-RS                | FastAPI                           |
| Dependency injection   | CDI (`@Inject`)                 | FastAPI `Depends()`               |
| ORM                    | Hibernate / Panache             | SQLAlchemy                        |
| Messaging              | MicroProfile Reactive Messaging | aiokafka                          |
| Data carriers (domain) | Java records                    | `dataclasses`                     |
| Data carriers (API)    | Java records                    | Pydantic `BaseModel`              |
| Testing                | JUnit + REST Assured            | pytest + FastAPI TestClient        |

## Package Structure

```
module-01-solution/
    config.py                                       # Environment configuration
    database.py                                     # SQLAlchemy engine and session setup
    conference/
        attendees/
            domain/
                events.py                           # AttendeeRegisteredEvent (frozen dataclass)
                aggregates.py                       # Attendee aggregate with factory method
                services.py                         # RegisterAttendeeCommand, AttendeeService
            infrastructure/
                dto.py                              # AttendeeDTO (Pydantic BaseModel)
                endpoint.py                         # FastAPI router (inbound adapter)
                event_publisher.py                  # Kafka publisher (outbound adapter)
            persistence/
                entity.py                           # AttendeeEntity (SQLAlchemy model)
                repository.py                       # AttendeeRepository
    tests/
        domain/
            test_events.py
            test_commands.py
            test_aggregates.py
            test_services.py
        persistence/
            test_repository.py
```

## DDD Building Blocks Covered

| Step | Building Block        | What It Does                                          |
|------|-----------------------|-------------------------------------------------------|
| 01   | Events                | Immutable facts that something happened               |
| 02   | Commands              | Intentions to perform a business operation            |
| 03   | Combining Returns     | Packaging aggregate + event as a result object        |
| 04   | Aggregates            | Business logic boundaries with factory methods        |
| 05   | Entities              | Persistence mapping (SQLAlchemy models)               |
| 06   | Repositories          | Collection-like interface to aggregates               |
| 07   | Outbound Adapters     | Technology adapters for external systems (Kafka)      |
| 08   | Application Services  | Workflow orchestration (no business logic)            |
| 09   | Data Transfer Objects | API contract objects (Pydantic models)                |
| 10   | Inbound Adapters      | REST endpoints translating HTTP to domain commands    |

## Getting Started

See the [README](README.md) for setup instructions and step-by-step navigation.
