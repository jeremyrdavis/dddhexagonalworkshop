"""
Anti-Corruption Layer translator.

An ANTICORRUPTION LAYER is an isolating layer to provide clients with
functionality in terms of their own domain model.
-- Eric Evans, Domain-Driven Design, 2003

This translator converts external Salesteam models into domain commands,
protecting the domain from external system contamination. All mapping
decisions (terminology, enum coercion, missing data) are centralized here.
"""

from conference.attendees.domain.services import RegisterAttendeeCommand
from conference.attendees.domain.valueobjects import MealPreference, TShirtSize
from conference.attendees.integration.salesteam.models import Customer, DietaryRequirements, Size


class SalesteamToDomainTranslator:
    """Translates Salesteam Customer objects into domain RegisterAttendeeCommands."""

    @staticmethod
    def translate(customers: list[Customer]) -> list[RegisterAttendeeCommand]:
        """Convert a list of Salesteam customers to domain commands."""
        return [SalesteamToDomainTranslator._translate_customer(c) for c in customers]

    @staticmethod
    def _translate_customer(customer: Customer) -> RegisterAttendeeCommand:
        """Convert a single Salesteam customer to a domain command."""
        return RegisterAttendeeCommand(
            email=customer.email,
            first_name=customer.first_name,
            last_name=customer.last_name,
            address=None,  # Salesteam does not provide addresses
            meal_preference=SalesteamToDomainTranslator._translate_dietary(
                customer.customer_details.dietary_requirements
            ),
            tshirt_size=SalesteamToDomainTranslator._translate_size(
                customer.customer_details.size
            ),
        )

    @staticmethod
    def _translate_dietary(dietary: DietaryRequirements) -> MealPreference:
        """Map Salesteam dietary requirements to domain meal preferences."""
        mapping = {
            DietaryRequirements.VEG: MealPreference.VEGETARIAN,
            DietaryRequirements.GLF: MealPreference.GLUTEN_FREE,
            DietaryRequirements.NA: MealPreference.NONE,
        }
        return mapping.get(dietary, MealPreference.NONE)

    @staticmethod
    def _translate_size(size: Size) -> TShirtSize:
        """Map Salesteam sizes to domain t-shirt sizes.

        Note: XS is coerced to S because the domain does not support XS.
        This is a business decision contained within the ACL.
        """
        mapping = {
            Size.XS: TShirtSize.S,  # Domain doesn't support XS — coerce to S
            Size.S: TShirtSize.S,
            Size.M: TShirtSize.M,
            Size.L: TShirtSize.L,
            Size.XL: TShirtSize.XL,
            Size.XXL: TShirtSize.XXL,
        }
        return mapping[size]
