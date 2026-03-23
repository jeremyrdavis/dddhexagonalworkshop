import dataclasses

import pytest

from conference.attendees.domain.valueobjects import Address, MealPreference, TShirtSize


class TestAddress:
    def test_address_creation(self):
        address = Address(
            street_address="1 Bag End",
            bus=None,
            postal_code="12345",
            town_or_municipality="Hobbiton",
        )
        assert address.street_address == "1 Bag End"
        assert address.bus is None
        assert address.postal_code == "12345"
        assert address.town_or_municipality == "Hobbiton"

    def test_address_with_bus(self):
        address = Address(
            street_address="1 Bag End",
            bus="Suite 2",
            postal_code="12345",
            town_or_municipality="Hobbiton",
        )
        assert address.bus == "Suite 2"

    def test_address_is_immutable(self):
        address = Address(
            street_address="1 Bag End",
            bus=None,
            postal_code="12345",
            town_or_municipality="Hobbiton",
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            address.street_address = "2 Bag End"

    def test_address_equality(self):
        address1 = Address(
            street_address="1 Bag End",
            bus=None,
            postal_code="12345",
            town_or_municipality="Hobbiton",
        )
        address2 = Address(
            street_address="1 Bag End",
            bus=None,
            postal_code="12345",
            town_or_municipality="Hobbiton",
        )
        assert address1 == address2

    def test_address_inequality(self):
        address1 = Address(
            street_address="1 Bag End",
            bus=None,
            postal_code="12345",
            town_or_municipality="Hobbiton",
        )
        address2 = Address(
            street_address="2 Bag End",
            bus=None,
            postal_code="12345",
            town_or_municipality="Hobbiton",
        )
        assert address1 != address2

    def test_address_rejects_blank_street(self):
        with pytest.raises(ValueError, match="Street address cannot be null or blank"):
            Address(
                street_address="",
                bus=None,
                postal_code="12345",
                town_or_municipality="Hobbiton",
            )

    def test_address_rejects_blank_postal_code(self):
        with pytest.raises(ValueError, match="Postal code cannot be null or blank"):
            Address(
                street_address="1 Bag End",
                bus=None,
                postal_code="",
                town_or_municipality="Hobbiton",
            )

    def test_address_rejects_blank_city(self):
        with pytest.raises(ValueError, match="City cannot be null or blank"):
            Address(
                street_address="1 Bag End",
                bus=None,
                postal_code="12345",
                town_or_municipality="",
            )


class TestMealPreference:
    def test_meal_preference_values(self):
        assert MealPreference.NONE.value == "NONE"
        assert MealPreference.VEGETARIAN.value == "VEGETARIAN"
        assert MealPreference.GLUTEN_FREE.value == "GLUTEN_FREE"

    def test_meal_preference_has_three_members(self):
        assert len(MealPreference) == 3


class TestTShirtSize:
    def test_tshirt_size_values(self):
        assert TShirtSize.S.value == "S"
        assert TShirtSize.M.value == "M"
        assert TShirtSize.L.value == "L"
        assert TShirtSize.XL.value == "XL"
        assert TShirtSize.XXL.value == "XXL"

    def test_tshirt_size_has_five_members(self):
        assert len(TShirtSize) == 5

    def test_tshirt_size_does_not_include_xs(self):
        with pytest.raises(ValueError):
            TShirtSize("XS")
