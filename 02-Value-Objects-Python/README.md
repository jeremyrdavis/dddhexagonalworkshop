# Module 02: Value Objects -- Python Port

A hands-on workshop module for learning the Value Objects pattern in Domain-Driven Design. This module extends the attendee registration system from Module 01 by adding an `Address` value object, first/last name fields, and richer domain modeling.

See the [Overview](Overview.md) for architecture details and background.

## Prerequisites

- Completed Module 01 (or start from `module-02-code/`, which includes the Module 01 solution)
- Python 3.11+
- PostgreSQL (or use SQLite for local development)
- Kafka (optional -- the application degrades gracefully without it)

## Setup

```bash
cd module-02-code

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
# .venv\Scripts\activate     # Windows

# Install dependencies
pip install -e ".[dev]"
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/domain/test_valueobjects.py

# Run a specific test class
pytest tests/domain/test_aggregates.py::TestAttendee
```

Tests use an in-memory SQLite database and mock objects for Kafka, so no external services are required.

## Running the Application

```bash
uvicorn main:app --reload
```

Then test the API:

```bash
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

## Workshop Steps

Work through these steps in order. Each step builds on the previous one.

| Step | Topic                                                   | File(s)                                                  |
|------|---------------------------------------------------------|----------------------------------------------------------|
| 01   | [Value Objects](01-Value-Objects.md)                    | `conference/attendees/domain/valueobjects.py`            |
| 02   | [Update the Command](02-Update-the-Command.md)         | `conference/attendees/domain/services.py`                |
| 03   | [Update the Aggregate](03-Update-the-Aggregate.md)     | `conference/attendees/domain/aggregates.py`              |
| 04   | [Update the Event](04-Update-the-Event.md)             | `conference/attendees/domain/events.py`                  |
| 05   | [Update Persistence](05-Update-Persistence.md)         | `conference/attendees/persistence/address_entity.py`, `entity.py`, `repository.py` |
| 06   | [Update the DTO](06-Update-the-DTO.md)                 | `conference/attendees/infrastructure/dto.py`             |
| 07   | [Update the Service](07-Update-the-Service.md)         | `conference/attendees/domain/services.py`, `endpoint.py`, `event_publisher.py` |

## Solution Code

The `module-02-solution/` directory contains the completed implementation for all 7 steps. If you get stuck, refer to the solution files.
