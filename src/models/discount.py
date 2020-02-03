#   Primary Author: Rahul Singh <rahulrsk07@gmail.com>
#
#   Purpose: This file contains the discount base class

from abc import abstractmethod
from typing import Any


class DiscountStrategy:
    """
    This is a base class for all discount strategies. All the discounts class will inherit this class.
    """

    @staticmethod
    def validate(discount_str: str) -> None:
        """
        Validates the discount string.

        Args:
            discount_str: discount string to be validated

        Returns:
            True if valid, else False
        """

        pass