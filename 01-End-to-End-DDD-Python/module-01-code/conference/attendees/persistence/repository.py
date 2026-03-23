from sqlalchemy.orm import Session


class AttendeeRepository:
    """
    A REPOSITORY represents all objects of a certain type as a conceptual set.
    It acts like an in-memory collection but is backed by a database.
    -- Eric Evans, Domain-Driven Design, 2003
    """

    def __init__(self, session: Session):
        self._session = session

    # TODO: Add persist() and _from_aggregate() methods
