#   Primary Author: Rahul Singh <rahulrsk07@gmail.com>
#
#   Purpose: This file contains base entity class and some basic abstract methods

from typing import Any
from abc import abstractmethod

from src.exceptions.exceptions import InvalidDiscountString
from src.models.discount import DiscountStrategy
from src.models.item_wise_discount import ItemWiseDiscountStrategy
from src.models.percentage_wise_discount import PercentageWiseDiscountStrategy


class Entity:
    """
    This is a base class for entities. All the entity class will inherit this class.
    """

    @abstractmethod
    def validate_args(self, *argv: Any) -> None:
        """
        Validates args for the entity.

        Returns:
            bool
        """

        pass

    @staticmethod
    def factory_for_discount(discount_str: str) -> DiscountStrategy():
        """
        This is a factory class for discount. This is will let us know what kind of discount has been provided.

        Args:
            discount_str: str containing discount data

        Returns:
            corresponding discount class
        """

        # if percentage is found in the str, use percentage discount strategy, else use item wise discount strategy
        if '%' in discount_str:
            return PercentageWiseDiscountStrategy

        if '+' in discount_str:
            return ItemWiseDiscountStrategy

        # raise exception if discount string doesn't match any format
        raise InvalidDiscountString

