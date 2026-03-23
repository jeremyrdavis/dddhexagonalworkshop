from pydantic import BaseModel


class AttendeeDTO(BaseModel):
    """
    Data Transfer Object for Attendee responses.

    DTOs are not specifically a DDD concept. They define the data contract
    between the API and its consumers, separate from the domain model.

    Note: The DTO includes full_name but NOT the address. This is a deliberate
    privacy decision — the address is collected for registration purposes but
    not exposed in API responses.
    """

    email: str
    full_name: str
