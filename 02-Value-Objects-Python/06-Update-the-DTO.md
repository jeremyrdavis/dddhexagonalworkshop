# Step 6: Update the AttendeeDTO

## TL;DR

Update `conference/attendees/infrastructure/dto.py`:

```python
from pydantic import BaseModel


class AttendeeDTO(BaseModel):
    email: str
    full_name: str
```

[Step 7: Update the AttendeeService](07-Update-the-Service.md)

## Overview

In this step, we update the `AttendeeDTO` to include the attendee's full name in API responses. This demonstrates how DTOs provide a stable interface for external communication while hiding internal domain complexity.

## Understanding DTOs in Hexagonal Architecture

DTOs serve as:

- **Anti-corruption Layer**: Protect domain models from external influence
- **Stable Interface**: Provide consistent API contracts regardless of internal changes
- **Data Shape Control**: Expose only the information needed by API consumers
- **Serialization Boundary**: Optimized for JSON serialization

## Implementation

Update `conference/attendees/infrastructure/dto.py`:

```python
from pydantic import BaseModel


class AttendeeDTO(BaseModel):
    """
    Data Transfer Object for Attendee responses.

    Note: The DTO includes full_name but NOT the address. This is a deliberate
    privacy decision -- the address is collected for registration purposes but
    not exposed in API responses.
    """

    email: str
    full_name: str
```

## Design Rationale

### What We Include

- **Email**: The primary identifier for the attendee
- **Full Name**: The computed full name from first and last names

### What We Don't Include

- **Address**: Sensitive information that should not be in every API response
- **Individual Name Components**: Clients typically need the full name rather than separate parts

### Why Not Include Address?

1. **Privacy**: Address information is sensitive and should only be exposed when necessary
2. **Performance**: Reduces payload size for list operations
3. **Flexibility**: Different endpoints can return different DTOs based on needs
4. **Security**: Principle of least privilege -- only expose what's needed

## JSON Response

The DTO will serialize to:

```json
{
  "email": "gandalfthegrey@istari.net",
  "full_name": "Gandalf Grey"
}
```

## Next Step

Continue to [Step 7: Update the AttendeeService](07-Update-the-Service.md)
