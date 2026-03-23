"""
External system models for the Salesteam integration.

These classes represent the Salesteam system's data structures and terminology.
They are NOT domain objects -- they exist only to deserialize incoming JSON
from the external system.
"""

# TODO: Add DietaryRequirements enum (VEG, GLF, NA)
# TODO: Add Size enum (XS, S, M, L, XL, XXL)
# TODO: Add CustomerDetails Pydantic model (dietary_requirements, size)
# TODO: Add Customer Pydantic model (first_name, last_name, email, employer, customer_details)
# TODO: Add SalesteamRegistrationRequest Pydantic model (customers: list[Customer])
