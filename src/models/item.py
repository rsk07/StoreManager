#   Primary Author: Rahul Singh <rahulrsk07@gmail.com>
#
#   Purpose: This file contains entity class for item

from typing import Any

from src.models.entity import Entity
from src.models.discount import DiscountStrategy
from src.models.sub_category import SubCategory
from src.enums import StandardUnits
from src.constants import units_mapping
from src.utilities import extract_required_data


class Item(Entity):
    def __init__(self, sub_category: SubCategory, name: str, price_str: str, discount_str: str) -> None:
        """
        Initialization method for item entity class.

        Args:
            sub_category: item's sub-category name
            name: item's name
            price_str: item's price str
            discount_str: items's discount string
        """

        self.sub_category = sub_category
        self.name = name
        self.price_per_unit, self.unit = self._extract_price_and_unit(price_str=price_str)
        self.discount_strategy = Entity.factory_for_discount(discount_str)(discount_str)

    @staticmethod
    def validate_args(*args: Any) -> bool:
        """
        Validates args for item entity.

        Args:
            *args: args to be validated

        Returns:
            True, if valid, else False
        """

        return len(args) == 4 and Item.validate_price(args[2]) and Entity.validate_discount(args[3])

    @staticmethod
    def validate_price(price_str: str) -> bool:
        """
        Validates the price string for item.

        Args:
            price_str: string to be validated

        Returns:
            True, if valid, else False
        """

        # if no digit is found, return false
        if not extract_required_data(data_str=price_str, req_type=r'\d+'):
            return False

        # if per('/') is not found, return false
        if '/' not in price_str:
            print("Please specify item price per ('/') units")
            return False

        # extract the unit from the price string
        unit = price_str[price_str.index('/') + 1:]

        # is unit not found in stored units, return false
        if not StandardUnits.has_value(unit) and unit not in units_mapping:
            return False

        return True

    def get_max_discount(self) -> int:
        """
        This will return the max discount between current entity and its parent class.

        Returns:
            max discount between current entity and its parent class
        """

        # return max discount between current entity and its parent class
        return max(self.discount_strategy.discount, self.sub_category.get_max_discount())

    def _extract_price_and_unit(self, price_str: str) -> tuple:
        """
        Extract item price per unit from the price string.

        Args:
            price_str: price string

        Returns:
            price, unit
        """

        # fetch the digits from the price string
        price = float(extract_required_data(data_str=price_str, req_type=r'[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)')[0])

        # fetch the unit
        unit = price_str[price_str.index('/') + 1:]

        # if a standard unit, return the same unit and price
        if StandardUnits.has_value(unit):
            return price, unit

        # if not a standard unit, convert the unit and price
        price /= units_mapping[unit]['std_equivalent_val']
        unit = units_mapping[unit]['std_equivalent_unit']

        return price, unit
