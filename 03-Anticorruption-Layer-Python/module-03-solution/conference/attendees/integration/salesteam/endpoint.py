"""
Salesteam integration endpoint.

This inbound adapter accepts bulk registration requests from the external
Salesteam system, translates them through the Anti-Corruption Layer, and
delegates to the domain service for each attendee.
"""

import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from conference.attendees.domain.services import AttendeeService
from conference.attendees.infrastructure.event_publisher import AttendeeEventPublisher
from conference.attendees.integration.salesteam.models import SalesteamRegistrationRequest
from conference.attendees.integration.salesteam.translator import SalesteamToDomainTranslator
from conference.attendees.persistence.repository import AttendeeRepository
from database import get_db

logger = logging.getLogger(__name__)

salesteam_router = APIRouter(prefix="/salesteam", tags=["salesteam"])


def get_attendee_service(db: Session = Depends(get_db)) -> AttendeeService:
    """Dependency injection: wire repository and event publisher into the service."""
    repository = AttendeeRepository(session=db)
    event_publisher = AttendeeEventPublisher(producer=None)
    return AttendeeService(repository=repository, event_publisher=event_publisher)


@salesteam_router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def register_from_salesteam(
    request: SalesteamRegistrationRequest,
    service: AttendeeService = Depends(get_attendee_service),
) -> dict:
    """
    Integration adapter: accepts bulk registrations from Salesteam,
    translates them through the ACL, and registers each attendee.
    """
    logger.debug("Received Salesteam registration for %d customers", len(request.customers))

    # Translate external models to domain commands via the ACL
    commands = SalesteamToDomainTranslator.translate(request.customers)

    # Register each attendee through the domain service
    for command in commands:
        await service.register_attendee(command)

    logger.info("Registered %d attendees from Salesteam", len(commands))
    return {"registered": len(commands)}
