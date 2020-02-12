#   Primary Author: Rahul Singh <rahulrsk07@gmail.com>
#
#   Purpose: This file contains the percentage wise discount class

from src.models.discount import DiscountStrategy


class PercentageWiseDiscountStrategy(DiscountStrategy):
    """
    This is the percentage wise discount strategy class
    """

    def __init__(self, discount_str: str) -> None:
        """
        Initialization method for percentage wise discount class.

        Args:
            discount_str: discount string containing the discount in percentage
        """

        self.discount = int(discount_str.strip('%'))

    @staticmethod
    def validate(discount_str: str) -> bool:
        """
        Validates the discount string.

        Args:
            discount_str:

        Returns:
            True if valid, else False
        """

        discount_temp = discount_str.strip('%')

        return discount_temp.isdigit() and (0 <= int(discount_temp) <= 100)