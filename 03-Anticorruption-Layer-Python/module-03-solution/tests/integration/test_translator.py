from conference.attendees.domain.valueobjects import MealPreference, TShirtSize
from conference.attendees.integration.salesteam.models import (
    Customer,
    CustomerDetails,
    DietaryRequirements,
    Size,
)
from conference.attendees.integration.salesteam.translator import SalesteamToDomainTranslator


def _customer(
    email="gandalf@istari.net",
    first_name="Gandalf",
    last_name="Grey",
    employer="Istari Inc",
    dietary=DietaryRequirements.NA,
    size=Size.L,
):
    return Customer(
        first_name=first_name,
        last_name=last_name,
        email=email,
        employer=employer,
        customer_details=CustomerDetails(dietary_requirements=dietary, size=size),
    )


class TestSalesteamToDomainTranslator:
    def test_translate_single_customer(self):
        commands = SalesteamToDomainTranslator.translate([_customer()])
        assert len(commands) == 1
        assert commands[0].email == "gandalf@istari.net"
        assert commands[0].first_name == "Gandalf"
        assert commands[0].last_name == "Grey"

    def test_translate_multiple_customers(self):
        customers = [
            _customer(email="gandalf@istari.net"),
            _customer(email="saruman@istari.net", first_name="Saruman", last_name="White"),
        ]
        commands = SalesteamToDomainTranslator.translate(customers)
        assert len(commands) == 2
        assert commands[0].email == "gandalf@istari.net"
        assert commands[1].email == "saruman@istari.net"

    def test_translate_address_is_none(self):
        commands = SalesteamToDomainTranslator.translate([_customer()])
        assert commands[0].address is None

    def test_translate_dietary_veg_to_vegetarian(self):
        commands = SalesteamToDomainTranslator.translate(
            [_customer(dietary=DietaryRequirements.VEG)]
        )
        assert commands[0].meal_preference == MealPreference.VEGETARIAN

    def test_translate_dietary_glf_to_gluten_free(self):
        commands = SalesteamToDomainTranslator.translate(
            [_customer(dietary=DietaryRequirements.GLF)]
        )
        assert commands[0].meal_preference == MealPreference.GLUTEN_FREE

    def test_translate_dietary_na_to_none(self):
        commands = SalesteamToDomainTranslator.translate(
            [_customer(dietary=DietaryRequirements.NA)]
        )
        assert commands[0].meal_preference == MealPreference.NONE

    def test_translate_size_xs_coerced_to_s(self):
        commands = SalesteamToDomainTranslator.translate([_customer(size=Size.XS)])
        assert commands[0].tshirt_size == TShirtSize.S

    def test_translate_size_s(self):
        commands = SalesteamToDomainTranslator.translate([_customer(size=Size.S)])
        assert commands[0].tshirt_size == TShirtSize.S

    def test_translate_size_xl(self):
        commands = SalesteamToDomainTranslator.translate([_customer(size=Size.XL)])
        assert commands[0].tshirt_size == TShirtSize.XL

    def test_translate_size_xxl(self):
        commands = SalesteamToDomainTranslator.translate([_customer(size=Size.XXL)])
        assert commands[0].tshirt_size == TShirtSize.XXL
