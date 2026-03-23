# Step 5: Update the Command

## TL;DR

Update `RegisterAttendeeCommand` in `conference/attendees/domain/services.py`:

```python
@dataclass(frozen=True)
class RegisterAttendeeCommand:
    email: str
    first_name: str
    last_name: str
    address: Address | None
    meal_preference: MealPreference
    tshirt_size: TShirtSize

    def __post_init__(self):
        if not self.email or self.email.strip() == "":
            raise ValueError("Email cannot be null or blank")
        if "@" not in self.email:
            raise ValueError("Email must contain @ symbol")
        if not self.first_name or self.first_name.strip() == "":
            raise ValueError("First name cannot be null or blank")
        if not self.last_name or self.last_name.strip() == "":
            raise ValueError("Last name cannot be null or blank")
```

Also update `infrastructure/endpoint.py` to add `meal_preference` and `tshirt_size` to the request model, and make `address` optional in `aggregates.py` and `persistence/entity.py`.

## Overview

In this final step, we update the `RegisterAttendeeCommand` to include the new value objects and make the address optional. These changes ripple through to the aggregate, persistence layer, and endpoint.

## Key Changes

### Command: Address becomes optional

```python
address: Address | None
```

The address validation (`if self.address is None: raise ValueError`) is removed. Salesteam registrations don't include addresses, so the command must accept `None`.

### Command: New value object fields

```python
meal_preference: MealPreference
tshirt_size: TShirtSize
```

These fields are required in the command but are **not passed to the aggregate**. In this iteration, the service drops them:

```python
result = Attendee.register_attendee(
    command.email, command.first_name, command.last_name, command.address
)
```

This is intentional -- the workshop focuses on the ACL pattern, not on fully wiring every field.

### Aggregate: Optional address

The `Attendee` aggregate's `__init__` and factory method accept `Address | None`.

### Persistence: Nullable FK

`AttendeeEntity.address_id` becomes nullable, and the repository handles `None` addresses.

### Endpoint: New request fields

`RegisterAttendeeRequest` adds `meal_preference: str` and `tshirt_size: str`, which are converted to domain enums in the endpoint handler.

## Verify Your Work

Run the full test suite:

```bash
pytest -v
```

All 56 tests should pass. Test both endpoints:

```bash
# Direct registration
curl -X POST http://localhost:8000/attendees/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "gandalf@istari.net",
    "first_name": "Gandalf",
    "last_name": "Grey",
    "address": {"street_address": "1 Bag End", "postal_code": "12345", "town_or_municipality": "Hobbiton"},
    "meal_preference": "VEGETARIAN",
    "tshirt_size": "L"
  }'

# Salesteam bulk registration
curl -X POST http://localhost:8000/salesteam/ \
  -H "Content-Type: application/json" \
  -d '{
    "customers": [{
      "first_name": "Gandalf", "last_name": "Grey",
      "email": "gandalf@istari.net", "employer": "Istari Inc",
      "customer_details": {"dietary_requirements": "VEG", "size": "XL"}
    }]
  }'
```

## Summary

In this module you learned:

- **Anti-Corruption Layer** protects your domain from external system contamination
- **Translators** map between external and domain terminology
- **External models** live in a separate `integration/` package, not in the domain
- **Domain purity** -- domain enums use plain `Enum`, external models use Pydantic
- **Business decisions** like size coercion (XS to S) live in the ACL, not the domain
- **Multiple entry points** can use the same domain service through different adapters
