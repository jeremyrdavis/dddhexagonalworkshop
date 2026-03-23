from conference.attendees.domain.aggregates import Attendee
from conference.attendees.domain.events import AttendeeRegisteredEvent
from conference.attendees.domain.services import AttendeeRegistrationResult


class TestAttendee:
    def test_register_attendee_returns_result(self):
        result = Attendee.register_attendee("gandalfthegrey@istari.net")
        assert isinstance(result, AttendeeRegistrationResult)

    def test_register_attendee_creates_aggregate(self):
        result = Attendee.register_attendee("gandalfthegrey@istari.net")
        assert result.attendee.email == "gandalfthegrey@istari.net"

    def test_register_attendee_creates_event(self):
        result = Attendee.register_attendee("gandalfthegrey@istari.net")
        assert isinstance(result.attendee_registered_event, AttendeeRegisteredEvent)
        assert result.attendee_registered_event.email == "gandalfthegrey@istari.net"
