# Python Port of Module 02 — Shaping Notes

## Scope

Port Module 02 (Value Objects, 7 steps) from Java/Quarkus to Python/FastAPI. Adds Address value object to the attendee registration system built in Module 01.

## Decisions

- Address fields match Java: street_address, bus, postal_code, town_or_municipality
- Domain layer uses frozen dataclass for Address (no framework deps)
- AddressEntity is a separate SQLAlchemy model with its own ID (database needs identity, value objects don't)
- Event includes full_name but NOT address (bounded context decision)
- DTO includes full_name but NOT address (privacy/API design decision)
- module-02-code starts as copy of Module 01 solution + stub files

## Context

- **Visuals:** None
- **References:** Java Module 02 at `02-Value-Objects/module-02-solution/`, Python Module 01 at `01-End-to-End-DDD-Python/module-01-solution/`
- **Product alignment:** Phase 1 MVP per `agent-os/product/roadmap.md`
