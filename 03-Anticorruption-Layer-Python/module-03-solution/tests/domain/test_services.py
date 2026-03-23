from unittest.mock import AsyncMock, MagicMock

import pytest

from conference.attendees.domain.services import AttendeeService, RegisterAttendeeCommand
from conference.attendees.domain.valueobjects import Address, MealPreference, TShirtSize
from conference.attendees.infrastructure.dto import AttendeeDTO


def _sample_address():
    return Address(
        street_address="1 Bag End",
        bus=None,
        postal_code="12345",
        town_or_municipality="Hobbiton",
    )


def _sample_command():
    return RegisterAttendeeCommand(
        email="gandalfthegrey@istari.net",
        first_name="Gandalf",
        last_name="Grey",
        address=_sample_address(),
        meal_preference=MealPreference.NONE,
        tshirt_size=TShirtSize.L,
    )


class TestAttendeeService:
    @pytest.fixture
    def mock_repository(self):
        return MagicMock()

    @pytest.fixture
    def mock_event_publisher(self):
        publisher = MagicMock()
        publisher.publish = AsyncMock()
        return publisher

    @pytest.fixture
    def service(self, mock_repository, mock_event_publisher):
        return AttendeeService(
            repository=mock_repository,
            event_publisher=mock_event_publisher,
        )

    @pytest.mark.asyncio
    async def test_register_attendee_persists(self, service, mock_repository):
        await service.register_attendee(_sample_command())
        mock_repository.persist.assert_called_once()

    @pytest.mark.asyncio
    async def test_register_attendee_publishes_event(self, service, mock_event_publisher):
        await service.register_attendee(_sample_command())
        mock_event_publisher.publish.assert_called_once()

    @pytest.mark.asyncio
    async def test_register_attendee_returns_dto(self, service):
        result = await service.register_attendee(_sample_command())
        assert isinstance(result, AttendeeDTO)
        assert result.email == "gandalfthegrey@istari.net"
        assert result.full_name == "Gandalf Grey"
