# Product Roadmap

## Phase 1: MVP

Port all three Quarkus modules to Python:

- **Module 01 — End-to-End DDD**: Events, Commands, Result Objects, Aggregates, Entities, Repositories, Outbound Adapters (Kafka), Application Services, DTOs, Inbound Adapters (REST)
- **Module 02 — Value Objects**: Address value object, updating commands/aggregates/events/persistence/DTOs/services to use value objects
- **Module 03 — Anti-Corruption Layer**: External system integration, translator, inbound adapter, value objects, command updates

Each module includes:
- Stubbed Python classes (`module-XX-code/`)
- Reference implementation (`module-XX-solution/`)
- Step-by-step markdown documentation
- TL;DR sections for quick copy/paste

## Phase 2: Post-Launch

- **Module 04 — Refactoring to DDD**: Port the MVC → DDD refactoring module, translating the Jakarta EE/WildFly example to a Python MVC framework (e.g., Flask or Django) being refactored toward Hexagonal Architecture
