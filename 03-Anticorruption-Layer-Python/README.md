# Module 03: Anti-Corruption Layer -- Python Port

A hands-on workshop module for learning the Anti-Corruption Layer pattern in Domain-Driven Design. This module extends the attendee registration system from Module 02 by integrating with an external "Salesteam" system that uses different terminology and data structures.

See the [Overview](Overview.md) for architecture details and background.

## Prerequisites

- Completed Module 02 (or start from `module-03-code/`, which includes the Module 02 solution)
- Python 3.11+
- PostgreSQL (or use SQLite for local development)
- Kafka (optional -- the application degrades gracefully without it)

## Setup

```bash
cd module-03-code

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

# Run translator tests only
pytest tests/integration/test_translator.py

# Run salesteam endpoint tests
pytest tests/integration/test_salesteam_endpoint.py
```

## Running the Application

```bash
uvicorn main:app --reload
```

Test the existing attendee endpoint:

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
    },
    "meal_preference": "VEGETARIAN",
    "tshirt_size": "L"
  }'
```

Test the new Salesteam integration endpoint:

```bash
curl -X POST http://localhost:8000/salesteam/ \
  -H "Content-Type: application/json" \
  -d '{
    "customers": [
      {
        "first_name": "Gandalf",
        "last_name": "Grey",
        "email": "gandalf@istari.net",
        "employer": "Istari Inc",
        "customer_details": {
          "dietary_requirements": "VEG",
          "size": "XL"
        }
      }
    ]
  }'
```

Expected response (HTTP 202):

```json
{"registered": 1}
```

## Workshop Steps

| Step | Topic                                                         | File(s)                                                  |
|------|---------------------------------------------------------------|----------------------------------------------------------|
| 01   | [The External System](01-The-External-System.md)              | `conference/attendees/integration/salesteam/models.py`   |
| 02   | [Implement a Translator](02-Implement-a-Translator.md)        | `conference/attendees/integration/salesteam/translator.py`|
| 03   | [Inbound Adapter](03-Inbound-Adapter.md)                      | `conference/attendees/integration/salesteam/endpoint.py`  |
| 04   | [Value Objects](04-Value-Objects.md)                          | `conference/attendees/domain/valueobjects.py`            |
| 05   | [Update the Command](05-Update-the-Command.md)                | `conference/attendees/domain/services.py`                |

## Solution Code

The `module-03-solution/` directory contains the completed implementation for all 5 steps.
