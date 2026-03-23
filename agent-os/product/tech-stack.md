# Tech Stack

## Backend

- **FastAPI** — REST API framework (inbound adapters)
- **Pydantic** — Data validation and serialization (DTOs, commands, events)
- **Python 3.11+** — Modern Python with dataclasses, type hints

## Database

- **PostgreSQL** — Primary data store
- **SQLAlchemy** — ORM for persistence layer (entities, repositories)
- **Alembic** — Database migrations (if needed)

## Messaging

- **aiokafka** or **confluent-kafka** — Kafka client for event publishing (outbound adapters)

## Development

- **uvicorn** — ASGI server for FastAPI
- **pytest** — Testing framework
- **Docker Compose** — Local PostgreSQL and Kafka for development
