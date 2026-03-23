# References for Python Port of Module 01

## Java Source Files (Reference Implementation)

All under `01-End-to-End-DDD/module-01-solution/src/main/java/dddhexagonalworkshop/conference/attendees/`:

### Domain Layer
- `domain/aggregates/Attendee.java` — Aggregate with static factory `registerAttendee(email)`
- `domain/events/AttendeeRegisteredEvent.java` — Immutable record
- `domain/services/AttendeeService.java` — Orchestrates persist + publish
- `domain/services/RegisterAttendeeCommand.java` — Immutable record with validation
- `domain/services/AttendeeRegistrationResult.java` — Immutable record (Attendee + Event)

### Infrastructure Layer
- `infrastructure/AttendeeEndpoint.java` — JAX-RS `@Path("/attendees")` POST endpoint
- `infrastructure/AttendeeDTO.java` — Immutable record for JSON response
- `infrastructure/AttendeeEventPublisher.java` — MicroProfile Kafka emitter

### Persistence Layer
- `persistence/AttendeeEntity.java` — JPA entity with auto-generated ID
- `persistence/AttendeeRepository.java` — PanacheRepository with aggregate conversion

## Step Documentation
- `01-End-to-End-DDD/01-Events.md` through `10-Inbound-Adapters.md` — Teaching structure reference
