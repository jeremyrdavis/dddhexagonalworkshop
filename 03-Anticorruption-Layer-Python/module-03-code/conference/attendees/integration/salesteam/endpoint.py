"""
Salesteam integration endpoint.

Accepts bulk registration requests from the external Salesteam system,
translates them through the Anti-Corruption Layer, and delegates to
the domain service.
"""

# TODO: Create a FastAPI router at /salesteam/
# TODO: Accept SalesteamRegistrationRequest
# TODO: Use SalesteamToDomainTranslator to convert to domain commands
# TODO: Call AttendeeService.register_attendee() for each command
# TODO: Return HTTP 202 Accepted
