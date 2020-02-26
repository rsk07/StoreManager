#   Primary Author: Rahul Singh <rahulrsk07@gmail.com>
#
#   Purpose: This file contains entity class for category

from typing import Any

from src.models.entity import Entity


class Category(Entity):
    """
    This is the category entity class.
    """

    def __init__(self, name: str, discount_str: str) -> None:
        """
        Initialization method for category entity class.

        Args:
            name: category's name
            discount_str: category's discount string
        """

        self.name = name
        self.discount_strategy = Entity.factory_for_discount(discount_str)(discount_str)

    @staticmethod
    def validate_args(*args: Any) -> bool:
        """
        Validates args for category entity.

        Args:
            *args: args to be validated

        Returns:
            True, if valid, else False
        """

        return len(args) == 2 and Entity.validate_discount(args[1])

    def get_max_discount(self) -> int:
        """
        This will return the max discount between current entity and its parent class.

        Returns:
            max discount between current entity and its parent class
        """

        # since category doesn't have a parent, return category's discount
        return self.discount_strategy.discount
