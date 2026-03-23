# Module 01: End-to-End DDD -- Python Port

A hands-on workshop for learning Domain-Driven Design and Hexagonal Architecture by building a conference attendee registration system in Python with FastAPI, SQLAlchemy, and aiokafka.

See the [Overview](Overview.md) for architecture details and background.

## Prerequisites

- Python 3.11+
- PostgreSQL (or use SQLite for local development)
- Kafka (optional -- the application degrades gracefully without it)

## Setup

```bash
cd module-01-solution

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
# .venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
# Or if using pyproject.toml:
# pip install -e ".[dev]"
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/domain/test_events.py

# Run a specific test class
pytest tests/domain/test_services.py::TestAttendeeService
```

Tests use an in-memory SQLite database and mock objects for Kafka, so no external services are required.

## Running the Application

```bash
# Start the FastAPI server
uvicorn main:app --reload

# Or if your entry point is different:
# uvicorn conference.attendees.infrastructure.endpoint:app --reload
```

Then test the API:

```bash
curl -X POST http://localhost:8000/attendees/ \
  -H "Content-Type: application/json" \
  -d '{"email": "gandalfthegrey@istari.net"}'
```

Expected response (HTTP 201):

```json
{"email": "gandalfthegrey@istari.net"}
```

## Workshop Steps

Work through these steps in order. Each step introduces one DDD building block and includes the complete code to add.

| Step | Topic                     | File                                              |
|------|---------------------------|---------------------------------------------------|
| 01   | [Events](01-Events.md)                             | `conference/attendees/domain/events.py`           |
| 02   | [Commands](02-Commands.md)                         | `conference/attendees/domain/services.py`         |
| 03   | [Combining Return Values](03-Combining-Return-Values.md) | `conference/attendees/domain/services.py`    |
| 04   | [Aggregates](04-Aggregates.md)                     | `conference/attendees/domain/aggregates.py`       |
| 05   | [Entities](05-Entities.md)                         | `conference/attendees/persistence/entity.py`      |
| 06   | [Repositories](06-Repositories.md)                 | `conference/attendees/persistence/repository.py`  |
| 07   | [Outbound Adapters](07-Outbound-Adapters.md)       | `conference/attendees/infrastructure/event_publisher.py` |
| 08   | [Application Services](08-Application-Services.md) | `conference/attendees/domain/services.py`        |
| 09   | [Data Transfer Objects](09-Data-Transfer-Objects.md) | `conference/attendees/infrastructure/dto.py`    |
| 10   | [Inbound Adapters](10-Inbound-Adapters.md)         | `conference/attendees/infrastructure/endpoint.py` |

## Solution Code

The `module-01-solution/` directory contains the completed implementation for all 10 steps. If you get stuck, refer to the solution files.

## Key Dependencies

| Package      | Purpose                                |
|--------------|----------------------------------------|
| `fastapi`    | Web framework and dependency injection |
| `uvicorn`    | ASGI server for FastAPI                |
| `sqlalchemy` | ORM and database session management    |
| `pydantic`   | Request/response models and validation |
| `aiokafka`   | Async Kafka producer for domain events |
| `pytest`     | Test framework                         |
| `pytest-asyncio` | Async test support for pytest     |
