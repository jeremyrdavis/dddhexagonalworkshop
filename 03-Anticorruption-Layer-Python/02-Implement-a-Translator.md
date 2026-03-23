# Step 2: Implement a Translator

## TL;DR

Create `conference/attendees/integration/salesteam/translator.py`:

```python
from conference.attendees.domain.services import RegisterAttendeeCommand
from conference.attendees.domain.valueobjects import MealPreference, TShirtSize
from conference.attendees.integration.salesteam.models import Customer, DietaryRequirements, Size


class SalesteamToDomainTranslator:
    @staticmethod
    def translate(customers: list[Customer]) -> list[RegisterAttendeeCommand]:
        return [SalesteamToDomainTranslator._translate_customer(c) for c in customers]

    @staticmethod
    def _translate_customer(customer: Customer) -> RegisterAttendeeCommand:
        return RegisterAttendeeCommand(
            email=customer.email,
            first_name=customer.first_name,
            last_name=customer.last_name,
            address=None,
            meal_preference=SalesteamToDomainTranslator._translate_dietary(
                customer.customer_details.dietary_requirements
            ),
            tshirt_size=SalesteamToDomainTranslator._translate_size(
                customer.customer_details.size
            ),
        )

    @staticmethod
    def _translate_dietary(dietary: DietaryRequirements) -> MealPreference:
        mapping = {
            DietaryRequirements.VEG: MealPreference.VEGETARIAN,
            DietaryRequirements.GLF: MealPreference.GLUTEN_FREE,
            DietaryRequirements.NA: MealPreference.NONE,
        }
        return mapping.get(dietary, MealPreference.NONE)

    @staticmethod
    def _translate_size(size: Size) -> TShirtSize:
        mapping = {
            Size.XS: TShirtSize.S,
            Size.S: TShirtSize.S,
            Size.M: TShirtSize.M,
            Size.L: TShirtSize.L,
            Size.XL: TShirtSize.XL,
            Size.XXL: TShirtSize.XXL,
        }
        return mapping[size]
```

[Step 3: Inbound Adapter](03-Inbound-Adapter.md)

## Learning Objectives

- Understand the Anti-Corruption Layer as a translation boundary
- Implement mapping between external and domain enums
- Handle data gaps (missing address) and coercion (XS to S)

## The Anti-Corruption Layer Pattern

> An ANTICORRUPTION LAYER is an isolating layer to provide clients with functionality in terms of their own domain model.
> -- Eric Evans, Domain-Driven Design, 2003

The translator is the core of the Anti-Corruption Layer. It takes external system objects and produces domain commands. The domain never sees the external models.

## Key Translation Decisions

### Dietary Requirements to Meal Preference

Salesteam uses abbreviated codes. The translator maps them to domain language:

| External | Domain |
|----------|--------|
| `VEG` | `VEGETARIAN` |
| `GLF` | `GLUTEN_FREE` |
| `NA` | `NONE` |

### Size Coercion

Salesteam supports XS, but our domain does not. The translator coerces XS to S:

```python
Size.XS: TShirtSize.S,  # Domain doesn't support XS — coerce to S
Size.S: TShirtSize.S,
```

This is a business decision that lives in the ACL, not in the domain. The domain doesn't know about this mapping.

### Missing Address

Salesteam does not provide attendee addresses. The translator sets `address=None`. This is why `address` becomes optional (`Address | None`) in the command and aggregate.

## Why Static Methods?

The translator uses static methods because it has no state. It's a pure function: given external objects, produce domain commands. No dependencies, no side effects.

## Next Step

Continue to [Step 3: Inbound Adapter](03-Inbound-Adapter.md)
