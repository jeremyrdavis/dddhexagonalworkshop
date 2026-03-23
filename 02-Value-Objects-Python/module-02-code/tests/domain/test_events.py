import dataclasses

import pytest

from conference.attendees.domain.events import AttendeeRegisteredEvent


class TestAttendeeRegisteredEvent:
    def test_event_contains_email(self):
        event = AttendeeRegisteredEvent(email="gandalfthegrey@istari.net")
        assert event.email == "gandalfthegrey@istari.net"

    def test_event_is_immutable(self):
        event = AttendeeRegisteredEvent(email="gandalfthegrey@istari.net")
        with pytest.raises(dataclasses.FrozenInstanceError):
            event.email = "sarumanthewhite@istari.net"

    def test_event_equality(self):
        event1 = AttendeeRegisteredEvent(email="gandalfthegrey@istari.net")
        event2 = AttendeeRegisteredEvent(email="gandalfthegrey@istari.net")
        assert event1 == event2
