from dataclasses import dataclass


@dataclass(frozen=True)
class Address:
    """
    A VALUE OBJECT is an object that describes some characteristic or attribute
    but carries no concept of identity.
    -- Eric Evans, Domain-Driven Design, 2003

    Value objects are defined by their attributes, not by an identity.
    Two addresses with the same fields are the same address.
    """

    pass  # TODO: Add street_address, bus, postal_code, town_or_municipality fields
    # TODO: Add __post_init__ validation for required fields
