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


def _salesteam_payload():
    return {
        "customers": [
            {
                "first_name": "Gandalf",
                "last_name": "Grey",
                "email": "gandalf@istari.net",
                "employer": "Istari Inc",
                "customer_details": {
                    "dietary_requirements": "VEG",
                    "size": "XL",
                },
            }
        ]
    }


class TestSalesteamEndpoint:
    def test_salesteam_returns_202(self, client):
        response = client.post("/salesteam/", json=_salesteam_payload())
        assert response.status_code == 202

    def test_salesteam_returns_count(self, client):
        response = client.post("/salesteam/", json=_salesteam_payload())
        assert response.json()["registered"] == 1

    def test_salesteam_registers_multiple_customers(self, client):
        payload = {
            "customers": [
                {
                    "first_name": "Gandalf",
                    "last_name": "Grey",
                    "email": "gandalf@istari.net",
                    "employer": "Istari Inc",
                    "customer_details": {"dietary_requirements": "VEG", "size": "XL"},
                },
                {
                    "first_name": "Saruman",
                    "last_name": "White",
                    "email": "saruman@istari.net",
                    "employer": "Istari Inc",
                    "customer_details": {"dietary_requirements": "NA", "size": "M"},
                },
            ]
        }
        response = client.post("/salesteam/", json=payload)
        assert response.status_code == 202
        assert response.json()["registered"] == 2

    def test_salesteam_with_xs_size(self, client):
        payload = {
            "customers": [
                {
                    "first_name": "Frodo",
                    "last_name": "Baggins",
                    "email": "frodo@shire.net",
                    "employer": "Bag End",
                    "customer_details": {"dietary_requirements": "NA", "size": "XS"},
                }
            ]
        }
        response = client.post("/salesteam/", json=payload)
        assert response.status_code == 202
