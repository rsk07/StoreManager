#   Primary Author: Rahul Singh <rahulrsk07@gmail.com>
#
#   Purpose: This file contains entity class for sub category

from typing import Any

from src.models.entity import Entity
from src.models.category import Category


class SubCategory(Entity):
    """
    This is the sub category entity class.
    """

    def __init__(self, category: Category, name: str, discount_str: str) -> None:
        """
        Initialization method for sub category entity class.

        Args:
            category: sub-category's category name
            name: sub category's name
            discount_str: sub category's discount string
        """

        self.category = category
        self.name = name
        self.discount_strategy = Entity.factory_for_discount(discount_str)(discount_str)

    @staticmethod
    def validate_args(*args: Any) -> bool:
        """
        Validates args for sub category entity.

        Args:
            *args: args to be validated

        Returns:
            True, if valid, else False
        """

        return len(args) == 3 and Entity.validate_discount(args[2])

    def get_max_discount(self) -> int:
        """
        This will return the max discount between current entity and its parent class.

        Returns:
            max discount between current entity and its parent class
        """

        # max discount between current entity and its parent class
        return max(self.discount_strategy.discount, self.category.get_max_discount())
