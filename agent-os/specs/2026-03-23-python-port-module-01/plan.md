# Plan: Port Module 01 (End-to-End DDD) to Python

See full plan at `.claude/plans/frolicking-inventing-clock.md`.

## Summary

Port the 10-step End-to-End DDD module from Java/Quarkus to Python/FastAPI. Creates both stubbed code (`module-01-code/`) and reference solutions (`module-01-solution/`) with fresh Python-specific documentation.

## Tech Stack

- FastAPI + uvicorn (REST)
- SQLAlchemy 2.0 (ORM)
- aiokafka (Kafka)
- Pydantic (DTOs/request models)
- dataclasses (domain layer)
- pytest (testing)

## 14 Tasks

1. Save spec docs
2. Project scaffolding
3-12. Port each workshop step (Events → Endpoint)
13. Write 10 markdown docs
14. Verification
