import dataclasses

import pytest

from conference.attendees.domain.services import RegisterAttendeeCommand
from conference.attendees.domain.valueobjects import Address, MealPreference, TShirtSize


def _sample_address():
    return Address(
        street_address="1 Bag End",
        bus=None,
        postal_code="12345",
        town_or_municipality="Hobbiton",
    )


def _sample_command(**overrides):
    defaults = {
        "email": "gandalfthegrey@istari.net",
        "first_name": "Gandalf",
        "last_name": "Grey",
        "address": _sample_address(),
        "meal_preference": MealPreference.NONE,
        "tshirt_size": TShirtSize.L,
    }
    defaults.update(overrides)
    return RegisterAttendeeCommand(**defaults)


class TestRegisterAttendeeCommand:
    def test_command_creation(self):
        command = _sample_command()
        assert command.email == "gandalfthegrey@istari.net"
        assert command.first_name == "Gandalf"
        assert command.last_name == "Grey"
        assert command.meal_preference == MealPreference.NONE
        assert command.tshirt_size == TShirtSize.L

    def test_command_accepts_null_address(self):
        command = _sample_command(address=None)
        assert command.address is None

    def test_command_rejects_blank_email(self):
        with pytest.raises(ValueError, match="Email cannot be null or blank"):
            _sample_command(email="")

    def test_command_rejects_whitespace_email(self):
        with pytest.raises(ValueError, match="Email cannot be null or blank"):
            _sample_command(email="   ")

    def test_command_rejects_email_without_at(self):
        with pytest.raises(ValueError, match="Email must contain @ symbol"):
            _sample_command(email="notanemail")

    def test_command_rejects_blank_first_name(self):
        with pytest.raises(ValueError, match="First name cannot be null or blank"):
            _sample_command(first_name="")

    def test_command_rejects_blank_last_name(self):
        with pytest.raises(ValueError, match="Last name cannot be null or blank"):
            _sample_command(last_name="")

    def test_command_is_immutable(self):
        command = _sample_command()
        with pytest.raises(dataclasses.FrozenInstanceError):
            command.email = "sarumanthewhite@istari.net"
