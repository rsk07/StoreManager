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