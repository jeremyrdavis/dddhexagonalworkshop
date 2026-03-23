# Module 03: Anti-Corruption Layer (Python)

## What You Will Build

In the previous modules you built a conference attendee registration system with Value Objects. This module introduces the **Anti-Corruption Layer (ACL)** pattern by integrating with an external system called "Salesteam" that sends bulk customer registrations using its own terminology and data structures.

The ACL creates a protective boundary between your domain model and external systems, ensuring your domain remains pure and uncontaminated by external concepts.

## The Problem

A corporate sales team uses a system called "Salesteam" to manage their customers. When they sponsor conference attendance for their employees, they send bulk registration requests. But Salesteam uses different terminology and data structures:

| Our Domain          | Salesteam's Language  |
|---------------------|-----------------------|
| Attendee            | Customer              |
| MealPreference      | DietaryRequirements   |
| `VEGETARIAN`        | `VEG`                 |
| `GLUTEN_FREE`       | `GLF`                 |
| `NONE`              | `NA`                  |
| TShirtSize (S-XXL)  | Size (XS-XXL)         |

If we let Salesteam's terminology leak into our domain, we end up with a messy model that speaks two languages. The ACL solves this.

## Anti-Corruption Layer Architecture

```
Salesteam (External System)
       |
       v
SalesteamEndpoint (POST /salesteam/)     <-- integration adapter
       |
       v
SalesteamToDomainTranslator.translate()  <-- ACL boundary
       |
       v
List[RegisterAttendeeCommand]            <-- domain commands
       |
       v
AttendeeService.register_attendee()      <-- domain service (existing)
```

The key insight: external system changes only affect the integration/translator layers. The domain never sees Salesteam's terminology.

## Key Design Decisions

### Size Coercion (XS to S)

Salesteam supports an "XS" size, but our domain does not. Rather than adding XS to our domain model (which would pollute it with an external concern), the translator coerces XS to S. This business decision lives in the ACL, not in the domain.

### No Address from Salesteam

Salesteam does not provide attendee addresses, so the translator sets `address=None`. This means `Address` becomes optional throughout the system.

### Terminology Translation

The translator maps between external abbreviations (`VEG`, `GLF`, `NA`) and domain language (`VEGETARIAN`, `GLUTEN_FREE`, `NONE`). This keeps the domain's ubiquitous language clean.

## What Changes from Module 02

### New Files

| File | Purpose |
|------|---------|
| `domain/valueobjects.py` | Add `MealPreference` and `TShirtSize` enums |
| `integration/salesteam/models.py` | External system data structures |
| `integration/salesteam/translator.py` | ACL translator (the core pattern) |
| `integration/salesteam/endpoint.py` | Integration REST endpoint |

### Modified Files

| File | Changes |
|------|---------|
| `domain/services.py` | Command adds `meal_preference` and `tshirt_size` |
| `domain/aggregates.py` | Address becomes optional (`Address \| None`) |
| `infrastructure/endpoint.py` | Request model adds new fields |
| `persistence/entity.py` | Address FK becomes nullable |
| `persistence/repository.py` | Handles null address |
| `main.py` | Includes salesteam router |

## Module Structure

| Step | Concept | What You Build | Key Learning |
|------|---------|----------------|--------------|
| 01 | [External System](01-The-External-System.md) | Salesteam models | Understanding external data |
| 02 | [Translator](02-Implement-a-Translator.md) | `SalesteamToDomainTranslator` | The ACL core |
| 03 | [Inbound Adapter](03-Inbound-Adapter.md) | `SalesteamEndpoint` | Integration endpoint |
| 04 | [Value Objects](04-Value-Objects.md) | `MealPreference`, `TShirtSize` | Domain enums |
| 05 | [Update Command](05-Update-the-Command.md) | `RegisterAttendeeCommand` | Evolving commands |

## Getting Started

See the [README](README.md) for setup instructions, then start with [Step 1: The External System](01-The-External-System.md).
