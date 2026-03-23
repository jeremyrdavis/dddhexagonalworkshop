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


def _valid_payload():
    return {
        "email": "gandalfthegrey@istari.net",
        "first_name": "Gandalf",
        "last_name": "Grey",
        "address": {
            "street_address": "1 Bag End",
            "postal_code": "12345",
            "town_or_municipality": "Hobbiton",
        },
    }


class TestAttendeeEndpoint:
    def test_register_attendee_returns_201(self, client):
        response = client.post("/attendees/", json=_valid_payload())
        assert response.status_code == 201

    def test_register_attendee_returns_email(self, client):
        response = client.post("/attendees/", json=_valid_payload())
        assert response.json()["email"] == "gandalfthegrey@istari.net"

    def test_register_attendee_returns_full_name(self, client):
        response = client.post("/attendees/", json=_valid_payload())
        assert response.json()["full_name"] == "Gandalf Grey"

    def test_register_attendee_rejects_invalid_email(self, client):
        payload = _valid_payload()
        payload["email"] = "notanemail"
        response = client.post("/attendees/", json=payload)
        assert response.status_code == 422

    def test_register_attendee_rejects_missing_address(self, client):
        response = client.post(
            "/attendees/",
            json={"email": "gandalfthegrey@istari.net", "first_name": "Gandalf", "last_name": "Grey"},
        )
        assert response.status_code == 422
