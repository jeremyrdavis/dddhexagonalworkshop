import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from conference.attendees.domain.aggregates import Attendee
from conference.attendees.domain.valueobjects import Address
from conference.attendees.persistence.entity import AttendeeEntity
from conference.attendees.persistence.repository import AttendeeRepository
from database import Base


def _sample_address():
    return Address(
        street_address="1 Bag End",
        bus=None,
        postal_code="12345",
        town_or_municipality="Hobbiton",
    )


@pytest.fixture
def session():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestSession = sessionmaker(bind=engine)
    session = TestSession()
    yield session
    session.close()


class TestAttendeeRepository:
    def test_persist_attendee(self, session):
        repo = AttendeeRepository(session=session)
        attendee = Attendee("gandalfthegrey@istari.net", "Gandalf", "Grey", _sample_address())

        repo.persist(attendee)
        session.commit()

        entity = session.query(AttendeeEntity).first()
        assert entity is not None
        assert entity.email == "gandalfthegrey@istari.net"
        assert entity.first_name == "Gandalf"
        assert entity.last_name == "Grey"
        assert entity.id is not None

    def test_persist_attendee_saves_address(self, session):
        repo = AttendeeRepository(session=session)
        attendee = Attendee("gandalfthegrey@istari.net", "Gandalf", "Grey", _sample_address())

        repo.persist(attendee)
        session.commit()

        entity = session.query(AttendeeEntity).first()
        assert entity.address is not None
        assert entity.address.street_address == "1 Bag End"
        assert entity.address.postal_code == "12345"
        assert entity.address.town_or_municipality == "Hobbiton"
