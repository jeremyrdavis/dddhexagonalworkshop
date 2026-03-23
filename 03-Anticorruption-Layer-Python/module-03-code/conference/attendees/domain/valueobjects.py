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

    street_address: str
    bus: str | None
    postal_code: str
    town_or_municipality: str

    def __post_init__(self):
        if not self.street_address or self.street_address.strip() == "":
            raise ValueError("Street address cannot be null or blank")
        if not self.postal_code or self.postal_code.strip() == "":
            raise ValueError("Postal code cannot be null or blank")
        if not self.town_or_municipality or self.town_or_municipality.strip() == "":
            raise ValueError("City cannot be null or blank")
