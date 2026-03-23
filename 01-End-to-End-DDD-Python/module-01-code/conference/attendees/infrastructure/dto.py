from pydantic import BaseModel


class AttendeeDTO(BaseModel):
    """
    Data Transfer Object for Attendee responses.

    DTOs are not specifically a DDD concept. They define the data contract
    between the API and its consumers, separate from the domain model.
    """

    pass  # TODO: Add the email field
