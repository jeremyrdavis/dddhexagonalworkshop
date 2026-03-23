class Attendee:
    """
    An AGGREGATE is a cluster of associated objects that we treat as a unit
    for the purpose of data changes.
    -- Eric Evans, Domain-Driven Design, 2003

    The Attendee aggregate encapsulates the business logic for attendee
    registration. It uses a factory method to ensure both the aggregate
    and the domain event are created together.
    """

    pass  # TODO: Add __init__, register_attendee classmethod, and email property
