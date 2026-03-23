"""
External system models for the Salesteam integration.

These classes represent the Salesteam system's data structures and terminology.
They are NOT domain objects -- they exist only to deserialize incoming JSON
from the external system.

Notice the terminology difference: Salesteam calls attendees "customers" and
uses abbreviated enum values (VEG, GLF, NA) that differ from our domain
language (VEGETARIAN, GLUTEN_FREE, NONE).
"""

from enum import Enum

from pydantic import BaseModel


class DietaryRequirements(str, Enum):
    """Salesteam's enum for dietary requirements (abbreviated notation)."""

    VEG = "VEG"
    GLF = "GLF"
    NA = "NA"


class Size(str, Enum):
    """Salesteam's enum for clothing sizes (includes XS, which our domain does not support)."""

    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"


class CustomerDetails(BaseModel):
    """Salesteam's nested details for a customer."""

    dietary_requirements: DietaryRequirements
    size: Size


class Customer(BaseModel):
    """Salesteam's representation of an attendee -- note the different terminology."""

    first_name: str
    last_name: str
    email: str
    employer: str
    customer_details: CustomerDetails


class SalesteamRegistrationRequest(BaseModel):
    """Wrapper for bulk registration requests from Salesteam."""

    customers: list[Customer]
