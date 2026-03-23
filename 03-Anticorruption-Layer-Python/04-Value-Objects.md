# Step 4: Value Objects

## TL;DR

Add to `conference/attendees/domain/valueobjects.py`:

```python
from enum import Enum


class MealPreference(Enum):
    NONE = "NONE"
    VEGETARIAN = "VEGETARIAN"
    GLUTEN_FREE = "GLUTEN_FREE"


class TShirtSize(Enum):
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"
```

[Step 5: Update the Command](05-Update-the-Command.md)

## Overview

In this step, we add two new domain value objects: `MealPreference` and `TShirtSize`. These are Python enums that live in the domain layer and use only domain language.

## Domain Enums vs. External Enums

Notice the contrast between domain and external enums:

| Domain (`valueobjects.py`) | External (`models.py`) |
|---------------------------|------------------------|
| `MealPreference(Enum)` | `DietaryRequirements(str, Enum)` |
| `VEGETARIAN` | `VEG` |
| `GLUTEN_FREE` | `GLF` |
| `NONE` | `NA` |
| `TShirtSize(Enum)` | `Size(str, Enum)` |
| 5 sizes (S-XXL) | 6 sizes (XS-XXL) |

Key differences:

- **Domain enums** use `Enum` (no framework dependency)
- **External enums** use `str, Enum` (Pydantic JSON deserialization)
- **Domain language** uses full words (`VEGETARIAN`, not `VEG`)
- **Domain has no XS** -- that's an external concept handled by the ACL

## Why Plain `Enum`?

Domain value objects should have zero framework dependencies. By using `enum.Enum` (standard library) instead of `str, Enum` (Pydantic pattern), we keep the domain pure. The external models need `str, Enum` because they parse JSON. The domain doesn't.

## Next Step

Continue to [Step 5: Update the Command](05-Update-the-Command.md)
