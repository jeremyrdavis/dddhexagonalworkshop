# Step 2: Commands

## TL;DR

Add the `RegisterAttendeeCommand` to `conference/attendees/domain/services.py`:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterAttendeeCommand:
    email: str

    def __post_init__(self):
        if not self.email or self.email.strip() == "":
            raise ValueError("Email cannot be null or blank")
        if "@" not in self.email:
            raise ValueError("Email must contain @ symbol")
```

[Step 3: Combining Return Values](03-Combining-Return-Values.md)

## Learning Objectives

- Understand how Commands encapsulate business intentions and requests for action
- Distinguish between Commands (can fail) and Events (facts that occurred)
- Implement a `RegisterAttendeeCommand` with validation using `__post_init__`

## What We Are Building

A `RegisterAttendeeCommand` frozen dataclass that encapsulates all the data needed to request attendee registration for the conference, along with validation that runs automatically at creation time.

## Why Commands Matter

Commands represent what a user or system *wants* to accomplish. Where an event says "this happened," a command says "please do this." That distinction is critical: commands can be rejected, while events cannot.

Commands provide a natural place to validate input before it reaches your business logic. Instead of scattering `if email is None` checks throughout your codebase, you centralize basic validation in the command itself. If someone tries to create a `RegisterAttendeeCommand` with a blank email, the command refuses to be constructed. The rest of your system never sees invalid data.

Commands are also immutable. Once created, a command cannot be modified as it passes through your system. This prevents an entire category of bugs where data changes between validation and processing. If you need different data, you create a new command.

## Implementation

The `RegisterAttendeeCommand` lives in the `conference/attendees/domain/services.py` module because it is part of the `AttendeeService`'s API. Commands are associated with the services that process them, keeping related concepts together.

Add the following to `conference/attendees/domain/services.py`:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterAttendeeCommand:
    """
    Commands encapsulate the intent to perform a business operation.
    Unlike events, commands can fail or be rejected.
    """

    # The email address of the attendee to register
    email: str

    def __post_init__(self):
        # Validate that the email is not blank or whitespace-only
        if not self.email or self.email.strip() == "":
            raise ValueError("Email cannot be null or blank")

        # Basic format check -- more sophisticated validation
        # belongs in the aggregate's business rules
        if "@" not in self.email:
            raise ValueError("Email must contain @ symbol")
```

### Why `__post_init__`?

In the Java version, commands use **compact constructors** -- a record feature where validation code runs automatically when the record is instantiated. Python's equivalent is `__post_init__`, a special method that dataclasses call immediately after `__init__` completes.

This means validation happens at construction time. You can never hold an invalid `RegisterAttendeeCommand` in your hands. If the email is blank or missing an `@` symbol, a `ValueError` is raised before the object finishes being created.

Note that `__post_init__` works with `frozen=True` because it runs during initialization, before the freeze takes effect. After construction, the object is truly immutable.

**Validation scope:** Keep command validation lightweight. Check that the data is syntactically valid (not blank, has an `@`). Complex business rules -- such as "is this attendee already registered?" -- belong in the Aggregate, which we will build in Step 4.

## Key Design Decisions

- **Frozen for safety.** Like events, commands are immutable. Once created, they cannot be modified. This prevents bugs where data changes between validation and processing.
- **Validation in `__post_init__`, not in the service.** Centralizing validation in the command means every code path that creates a command gets the same checks. No caller can bypass validation.
- **`ValueError` for invalid input.** Python convention uses `ValueError` for arguments that are the wrong value. This is the natural equivalent of Java's `IllegalArgumentException`.

### Commands vs Events: A Critical Distinction

| Aspect         | Commands                | Events                    |
|----------------|-------------------------|---------------------------|
| **Nature**     | Intention / Request     | Fact / What happened      |
| **Can fail?**  | Yes                     | No (already happened)     |
| **Mutability** | Immutable               | Immutable                 |
| **Tense**      | Imperative ("Register") | Past tense ("Registered") |
| **Example**    | `RegisterAttendeeCommand` | `AttendeeRegisteredEvent` |

Think of it like ordering food:

- **Command**: "I want to order a burger" (the restaurant might be out of burgers)
- **Event**: "Customer ordered a burger at 2:15 PM" (this definitely happened)

## Testing Your Implementation

Create or update `tests/domain/test_commands.py`:

```python
import dataclasses

import pytest

from conference.attendees.domain.services import RegisterAttendeeCommand


class TestRegisterAttendeeCommand:
    def test_command_creation(self):
        """A valid command should store the provided email."""
        command = RegisterAttendeeCommand(email="gandalfthegrey@istari.net")
        assert command.email == "gandalfthegrey@istari.net"

    def test_command_rejects_blank_email(self):
        """An empty string is not a valid email."""
        with pytest.raises(ValueError, match="Email cannot be null or blank"):
            RegisterAttendeeCommand(email="")

    def test_command_rejects_whitespace_email(self):
        """A whitespace-only string is not a valid email."""
        with pytest.raises(ValueError, match="Email cannot be null or blank"):
            RegisterAttendeeCommand(email="   ")

    def test_command_rejects_email_without_at(self):
        """An email without @ is not valid."""
        with pytest.raises(ValueError, match="Email must contain @ symbol"):
            RegisterAttendeeCommand(email="notanemail")

    def test_command_is_immutable(self):
        """Commands must not be modified after creation."""
        command = RegisterAttendeeCommand(email="gandalfthegrey@istari.net")
        with pytest.raises(dataclasses.FrozenInstanceError):
            command.email = "sarumanthewhite@istari.net"
```

Run the tests:

```bash
pytest tests/domain/test_commands.py -v
```

All five tests should pass, confirming that the command stores valid data, rejects invalid data, and cannot be modified after creation.

## Next Steps

In the next step, we will create the `AttendeeRegistrationResult` that packages together the outputs of processing this command -- both the created `Attendee` and the `AttendeeRegisteredEvent` that needs to be published: [Step 3: Combining Return Values](03-Combining-Return-Values.md)
