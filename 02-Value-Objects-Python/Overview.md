# Module 02: Value Objects (Python)

## What You Will Build

In the first module you built an end-to-end workflow for conference attendee registration. This module extends that application by introducing the **Value Objects** pattern -- a fundamental building block of Domain-Driven Design. By the end you will have added an `Address` value object to the attendee registration system, along with first and last name fields.

## Core DDD Concepts Covered

### Value Objects

Value Objects are objects that describe the state of something else. They are not Entities, which have continuity and identify something that is tracked over time.

- **Value Objects** are equal based on their **value**
- **Entities** are equal based on their **identifier**

An address is a classic example of a Value Object. Two addresses with the same street, postal code, and city are the same address -- there is no separate "address identity" that distinguishes them.

### Aggregates

Business entities that encapsulate logic and maintain consistency within their boundaries. In this module we extend the Attendee aggregate with richer fields.

### Events and Commands

- **Events**: Record facts that have already occurred (immutable) and most importantly _what the business cares about_.
- **Commands**: Represent intentions to change state (can fail)

### Information Hiding Across Bounded Contexts

A key design decision in this module: the `AttendeeRegisteredEvent` and `AttendeeDTO` include the attendee's `full_name` but **not** their address. This is deliberate -- the address is internal to the attendee context and should not be broadcast to every subscriber.

## What Changes from Module 01

### New Files

| File | Purpose |
|------|---------|
| `domain/valueobjects.py` | `Address` frozen dataclass with validation |
| `persistence/address_entity.py` | SQLAlchemy model for the `attendee_address` table |

### Modified Files

| File | Changes |
|------|---------|
| `domain/services.py` | `RegisterAttendeeCommand` adds `first_name`, `last_name`, `address` |
| `domain/aggregates.py` | `Attendee` adds fields, `full_name` property, updated factory |
| `domain/events.py` | `AttendeeRegisteredEvent` adds `full_name` |
| `persistence/entity.py` | `AttendeeEntity` adds name fields and FK to `AddressEntity` |
| `persistence/repository.py` | Converts `Address` value object to `AddressEntity` |
| `infrastructure/dto.py` | `AttendeeDTO` adds `full_name` |
| `infrastructure/endpoint.py` | Adds `AddressRequest` Pydantic model, updates request handling |
| `infrastructure/event_publisher.py` | Serializes `full_name` in Kafka JSON |
| `main.py` | Imports `AddressEntity` for table creation |

## Module Structure

| Step | Concept | What You Build | Key Learning |
|------|---------|----------------|--------------|
| 01 | [Value Objects](01-Value-Objects.md) | `Address` | The role of value objects |
| 02 | [Commands](02-Update-the-Command.md) | `RegisterAttendeeCommand` | Evolving commands |
| 03 | [Aggregates](03-Update-the-Aggregate.md) | `Attendee` | Aggregate design |
| 04 | [Events](04-Update-the-Event.md) | `AttendeeRegisteredEvent` | Information hiding |
| 05 | [Persistence](05-Update-Persistence.md) | `AttendeeEntity`, `AddressEntity` | Object-relational impedance mismatch |
| 06 | [DTOs](06-Update-the-DTO.md) | `AttendeeDTO` | Privacy in API responses |
| 07 | [Services](07-Update-the-Service.md) | `AttendeeService` | Wiring it all together |

### Learning Approach

Each step follows a consistent pattern:

- **TL;DR**: A quick implementation reference with no explanation
- **Concept Explanation**: Why this pattern matters
- **Hands-On Implementation**: Code with detailed explanations

If you get stuck, refer to the `module-02-solution/` directory or ask for help.

## Getting Started

See the [README](README.md) for setup instructions, then start with [Step 1: Value Objects](01-Value-Objects.md).
