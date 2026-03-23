# Python Port of Module 01 — Shaping Notes

## Scope

Port Module 01 (End-to-End DDD, 10 steps) from Java/Quarkus to Python/FastAPI. Produce stubbed code, reference solutions, and fresh Python-specific step documentation.

## Decisions

- Domain layer uses stdlib `dataclasses(frozen=True)` — zero framework deps
- Infrastructure layer uses Pydantic `BaseModel` for DTOs and request models
- Endpoint translates Pydantic request → domain dataclass command (boundary translation)
- Async Kafka publisher (aiokafka), sync domain/repository
- SQLAlchemy 2.0 `DeclarativeBase` for entities
- Tests use SQLite in-memory (no PostgreSQL required)
- Python-idiomatic project layout with `pyproject.toml` (not Maven-style `src/`)
- Fresh documentation rather than adapting Java docs

## Context

- **Visuals:** None
- **References:** Java Module 01 solution at `01-End-to-End-DDD/module-01-solution/`
- **Product alignment:** Phase 1 MVP per `agent-os/product/roadmap.md`

## Standards Applied

No standards defined yet in `agent-os/standards/index.yml`.
