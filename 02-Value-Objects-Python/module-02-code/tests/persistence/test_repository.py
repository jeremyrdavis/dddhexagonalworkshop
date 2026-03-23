import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from conference.attendees.domain.aggregates import Attendee
from conference.attendees.persistence.entity import AttendeeEntity
from conference.attendees.persistence.repository import AttendeeRepository
from database import Base


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
        attendee = Attendee("gandalfthegrey@istari.net")

        repo.persist(attendee)
        session.commit()

        entity = session.query(AttendeeEntity).first()
        assert entity is not None
        assert entity.email == "gandalfthegrey@istari.net"
        assert entity.id is not None
