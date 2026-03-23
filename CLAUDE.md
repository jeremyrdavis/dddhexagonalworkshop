# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A hands-on workshop for learning Domain-Driven Design (DDD) and Hexagonal Architecture by building a conference attendee registration system.

- **Modules 01-03**: Quarkus 3.23.0, Java 21, Hibernate Panache, Kafka
- **Module 04**: Jakarta EE 10 / WildFly, Java 11, traditional MVC → DDD refactoring

## Repository Structure

```
01-End-to-End-DDD/         # Complete DDD workflow (10 steps)
02-Value-Objects/          # Value Objects pattern (7 steps)
03-Anticorruption-Layer/   # Anti-corruption layer pattern (5 steps)
04-Refactoring-to-DDD/     # Traditional MVC → DDD refactoring (Jakarta EE/WildFly)
```

Each module (01-03) has `module-XX-code/` (stubbed starting point) and `module-XX-solution/` (reference implementation), plus step-by-step markdown docs (e.g., `04-Aggregates.md`).

## Build and Development Commands

### Modules 01-03 (Quarkus)

All commands run from within a module directory (e.g., `cd 01-End-to-End-DDD/module-01-code`).

```bash
./mvnw quarkus:dev          # Dev mode (auto-starts PostgreSQL + Kafka)
./mvnw clean compile        # Compile only
./mvnw test                 # Run all tests
./mvnw clean package        # Full build

# Run a single test class
./mvnw test -Dtest=AttendeeTest

# Run a single test method
./mvnw test -Dtest=AttendeeTest#testRegisterAttendee
```

### Module 04 (Jakarta EE/WildFly)

```bash
cd 04-Refactoring-to-DDD
mvn clean package           # Build WAR
docker-compose up --build   # Run with Docker Compose
```

## Architecture

Hexagonal Architecture (Ports & Adapters):

```
HTTP Requests → REST Endpoint (inbound adapter) → Domain Service → Aggregate
                                                                  ↓
                                              Repository (outbound adapter) → Database
                                              EventPublisher (outbound adapter) → Kafka
```

### Package Structure (Modules 01-03)

Base package: `dddhexagonalworkshop.conference.attendees`

- `domain/aggregates/` — Attendee aggregate (pure business logic, no framework dependencies)
- `domain/events/` — AttendeeRegisteredEvent (immutable domain facts)
- `domain/services/` — AttendeeService (workflow orchestration), RegisterAttendeeCommand, AttendeeRegistrationResult
- `infrastructure/` — Inbound adapter (AttendeeEndpoint), DTO (AttendeeDTO), Outbound adapter (AttendeeEventPublisher)
- `persistence/` — AttendeeEntity (JPA entity, separate from domain aggregate), AttendeeRepository

### Key Design Rules

1. Domain layer has zero framework dependencies — pure Java
2. Aggregates encapsulate business rules; Commands can fail, Events are immutable facts
3. JPA entities are separate from domain aggregates (persistence/domain boundary)
4. Adapters isolate domain from REST, database, and Kafka concerns

## Workshop Pedagogy

When helping with workshop code:
- Reference the step documentation (e.g., `01-End-to-End-DDD/04-Aggregates.md`)
- Guide users to implement patterns correctly rather than just providing solutions
- Each step should compile successfully — verify with `./mvnw clean compile`
- If stuck, direct to the `module-XX-solution/` directory
- Each step has a TL;DR section with just the code for quick copy/paste

## Development Environment

`devfile.yaml` provisions GitHub Codespaces / OpenShift Dev Spaces with Java 21, PostgreSQL 16, and Kafka 3.6. In local development, `./mvnw quarkus:dev` handles all dependencies automatically via Quarkus DevServices.
