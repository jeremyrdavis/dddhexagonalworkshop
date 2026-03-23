import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/attendees", tags=["attendees"])


# TODO: Add RegisterAttendeeRequest Pydantic model
# TODO: Add get_attendee_service dependency function
# TODO: Add POST route handler for attendee registration
