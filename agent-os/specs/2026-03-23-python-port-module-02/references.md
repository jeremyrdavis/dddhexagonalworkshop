# References for Python Port of Module 02

## Java Source Files

All under `02-Value-Objects/module-02-solution/src/main/java/dddhexagonalworkshop/conference/attendees/`:

### NEW in Module 02
- `domain/valueobjects/Address.java` — Immutable record with validation
- `persistence/AddressEntity.java` — JPA entity with own ID

### Modified from Module 01
- `domain/aggregates/Attendee.java` — Added firstName, lastName, address, getFullName()
- `domain/events/AttendeeRegisteredEvent.java` — Added fullName
- `domain/services/RegisterAttendeeCommand.java` — Added firstName, lastName, address
- `domain/services/AttendeeService.java` — Passes new fields
- `persistence/AttendeeEntity.java` — Added fields + @OneToOne to AddressEntity
- `persistence/AttendeeRepository.java` — Address → AddressEntity conversion
- `infrastructure/AttendeeDTO.java` — Added fullName

## Python Starting Point
- `01-End-to-End-DDD-Python/module-01-solution/` — All files copied as Module 02 base
