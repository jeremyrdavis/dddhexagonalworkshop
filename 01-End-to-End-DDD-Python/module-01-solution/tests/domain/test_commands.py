import dataclasses

import pytest

from conference.attendees.domain.services import RegisterAttendeeCommand


class TestRegisterAttendeeCommand:
    def test_command_creation(self):
        command = RegisterAttendeeCommand(email="gandalfthegrey@istari.net")
        assert command.email == "gandalfthegrey@istari.net"

    def test_command_rejects_blank_email(self):
        with pytest.raises(ValueError, match="Email cannot be null or blank"):
            RegisterAttendeeCommand(email="")

    def test_command_rejects_whitespace_email(self):
        with pytest.raises(ValueError, match="Email cannot be null or blank"):
            RegisterAttendeeCommand(email="   ")

    def test_command_rejects_email_without_at(self):
        with pytest.raises(ValueError, match="Email must contain @ symbol"):
            RegisterAttendeeCommand(email="notanemail")

    def test_command_is_immutable(self):
        command = RegisterAttendeeCommand(email="gandalfthegrey@istari.net")
        with pytest.raises(dataclasses.FrozenInstanceError):
            command.email = "sarumanthewhite@istari.net"
