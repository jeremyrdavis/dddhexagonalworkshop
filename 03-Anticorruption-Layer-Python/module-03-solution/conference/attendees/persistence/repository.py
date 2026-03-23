from sqlalchemy.orm import Session

from conference.attendees.domain.aggregates import Attendee
from conference.attendees.persistence.address_entity import AddressEntity
from conference.attendees.persistence.entity import AttendeeEntity


class AttendeeRepository:
    """
    A REPOSITORY represents all objects of a certain type as a conceptual set.
    It acts like an in-memory collection but is backed by a database.
    -- Eric Evans, Domain-Driven Design, 2003
    """

    def __init__(self, session: Session):
        self._session = session

    def persist(self, aggregate: Attendee) -> None:
        """Transform the aggregate to an entity and persist it."""
        entity = self._from_aggregate(aggregate)
        self._session.add(entity)
        self._session.flush()

    def _from_aggregate(self, attendee: Attendee) -> AttendeeEntity:
        """Convert a domain aggregate to a persistence entity."""
        address_entity = None
        if attendee.address is not None:
            address_entity = AddressEntity(
                street_address=attendee.address.street_address,
                bus=attendee.address.bus,
                postal_code=attendee.address.postal_code,
                town_or_municipality=attendee.address.town_or_municipality,
            )
        return AttendeeEntity(
            email=attendee.email,
            first_name=attendee.first_name,
            last_name=attendee.last_name,
            address=address_entity,
        )
