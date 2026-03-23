import dataclasses

import pytest

from conference.attendees.domain.services import RegisterAttendeeCommand
from conference.attendees.domain.valueobjects import Address


def _sample_address():
    return Address(
        street_address="1 Bag End",
        bus=None,
        postal_code="12345",
        town_or_municipality="Hobbiton",
    )


class TestRegisterAttendeeCommand:
    def test_command_creation(self):
        command = RegisterAttendeeCommand(
            email="gandalfthegrey@istari.net",
            first_name="Gandalf",
            last_name="Grey",
            address=_sample_address(),
        )
        assert command.email == "gandalfthegrey@istari.net"
        assert command.first_name == "Gandalf"
        assert command.last_name == "Grey"

    def test_command_rejects_blank_email(self):
        with pytest.raises(ValueError, match="Email cannot be null or blank"):
            RegisterAttendeeCommand(
                email="", first_name="Gandalf", last_name="Grey", address=_sample_address()
            )

    def test_command_rejects_whitespace_email(self):
        with pytest.raises(ValueError, match="Email cannot be null or blank"):
            RegisterAttendeeCommand(
                email="   ", first_name="Gandalf", last_name="Grey", address=_sample_address()
            )

    def test_command_rejects_email_without_at(self):
        with pytest.raises(ValueError, match="Email must contain @ symbol"):
            RegisterAttendeeCommand(
                email="notanemail", first_name="Gandalf", last_name="Grey", address=_sample_address()
            )

    def test_command_rejects_blank_first_name(self):
        with pytest.raises(ValueError, match="First name cannot be null or blank"):
            RegisterAttendeeCommand(
                email="gandalfthegrey@istari.net", first_name="", last_name="Grey", address=_sample_address()
            )

    def test_command_rejects_blank_last_name(self):
        with pytest.raises(ValueError, match="Last name cannot be null or blank"):
            RegisterAttendeeCommand(
                email="gandalfthegrey@istari.net", first_name="Gandalf", last_name="", address=_sample_address()
            )

    def test_command_is_immutable(self):
        command = RegisterAttendeeCommand(
            email="gandalfthegrey@istari.net",
            first_name="Gandalf",
            last_name="Grey",
            address=_sample_address(),
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            command.email = "sarumanthewhite@istari.net"
