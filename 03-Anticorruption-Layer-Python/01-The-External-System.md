# Step 1: The External System

## TL;DR

Create `conference/attendees/integration/salesteam/models.py`:

```python
from enum import Enum
from pydantic import BaseModel


class DietaryRequirements(str, Enum):
    VEG = "VEG"
    GLF = "GLF"
    NA = "NA"


class Size(str, Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"


class CustomerDetails(BaseModel):
    dietary_requirements: DietaryRequirements
    size: Size


class Customer(BaseModel):
    first_name: str
    last_name: str
    email: str
    employer: str
    customer_details: CustomerDetails


class SalesteamRegistrationRequest(BaseModel):
    customers: list[Customer]
```

[Step 2: Implement a Translator](02-Implement-a-Translator.md)

## Learning Objectives

- Understand external system models and their role in integration
- Recognize terminology differences between systems
- Model external data structures without contaminating the domain

## Why Separate External Models?

When integrating with an external system, the first step is to model that system's data structures _in their own package_. These classes represent the external system's "ubiquitous language" -- not yours.

Notice the terminology differences:

| Our Domain | Salesteam |
|-----------|-----------|
| Attendee | Customer |
| MealPreference | DietaryRequirements |
| VEGETARIAN | VEG |
| GLUTEN_FREE | GLF |
| NONE | NA |
| TShirtSize (5 values) | Size (6 values, includes XS) |

These external models live in `integration/salesteam/`, completely separate from the domain. They use Pydantic `BaseModel` because they need to deserialize JSON from HTTP requests -- they are boundary objects, not domain objects.

## Implementation

Create the package structure:

```
conference/attendees/integration/
    __init__.py
    salesteam/
        __init__.py
        models.py
```

Then create `conference/attendees/integration/salesteam/models.py` with the external models.

### Why `str, Enum`?

The external enums inherit from both `str` and `Enum`. This is a Pydantic pattern that allows enum values to be automatically deserialized from JSON strings. When Salesteam sends `"VEG"` in their JSON, Pydantic converts it to `DietaryRequirements.VEG`.

### Why Pydantic for external models?

External system models exist at the HTTP boundary. They parse incoming JSON, so Pydantic is the right tool. Domain value objects use plain `enum.Enum` because they have no framework dependencies.

## Next Step

Continue to [Step 2: Implement a Translator](02-Implement-a-Translator.md)
