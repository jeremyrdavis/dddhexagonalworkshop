from conference.attendees.domain.aggregates import Attendee
from conference.attendees.domain.events import AttendeeRegisteredEvent
from conference.attendees.domain.services import AttendeeRegistrationResult
from conference.attendees.domain.valueobjects import Address


def _sample_address():
    return Address(
        street_address="1 Bag End",
        bus=None,
        postal_code="12345",
        town_or_municipality="Hobbiton",
    )


class TestAttendee:
    def test_register_attendee_returns_result(self):
        result = Attendee.register_attendee(
            "gandalfthegrey@istari.net", "Gandalf", "Grey", _sample_address()
        )
        assert isinstance(result, AttendeeRegistrationResult)

    def test_register_attendee_creates_aggregate(self):
        result = Attendee.register_attendee(
            "gandalfthegrey@istari.net", "Gandalf", "Grey", _sample_address()
        )
        assert result.attendee.email == "gandalfthegrey@istari.net"
        assert result.attendee.first_name == "Gandalf"
        assert result.attendee.last_name == "Grey"

    def test_register_attendee_creates_event(self):
        result = Attendee.register_attendee(
            "gandalfthegrey@istari.net", "Gandalf", "Grey", _sample_address()
        )
        assert isinstance(result.attendee_registered_event, AttendeeRegisteredEvent)
        assert result.attendee_registered_event.email == "gandalfthegrey@istari.net"
        assert result.attendee_registered_event.full_name == "Gandalf Grey"

    def test_full_name_property(self):
        result = Attendee.register_attendee(
            "gandalfthegrey@istari.net", "Gandalf", "Grey", _sample_address()
        )
        assert result.attendee.full_name == "Gandalf Grey"

    def test_address_is_stored(self):
        address = _sample_address()
        result = Attendee.register_attendee(
            "gandalfthegrey@istari.net", "Gandalf", "Grey", address
        )
        assert result.attendee.address == address

    def test_register_attendee_with_null_address(self):
        result = Attendee.register_attendee(
            "gandalfthegrey@istari.net", "Gandalf", "Grey", None
        )
        assert result.attendee.address is None
