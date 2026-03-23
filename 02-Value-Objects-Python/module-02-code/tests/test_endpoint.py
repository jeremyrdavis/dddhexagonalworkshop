import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app


@pytest.fixture
def client():
    """Create a test client with an in-memory SQLite database."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestSession = sessionmaker(bind=engine)

    def override_get_db():
        session = TestSession()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    app.state.engine = engine

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


class TestAttendeeEndpoint:
    def test_register_attendee_returns_201(self, client):
        response = client.post(
            "/attendees/",
            json={"email": "gandalfthegrey@istari.net"},
        )
        assert response.status_code == 201

    def test_register_attendee_returns_email(self, client):
        response = client.post(
            "/attendees/",
            json={"email": "gandalfthegrey@istari.net"},
        )
        assert response.json()["email"] == "gandalfthegrey@istari.net"

    def test_register_attendee_rejects_invalid_email(self, client):
        response = client.post(
            "/attendees/",
            json={"email": "notanemail"},
        )
        assert response.status_code == 422
