#   Primary Author: Rahul Singh <rahulrsk07@gmail.com>
#
#   Purpose: This file contains the item wise discount class

from src.models.discount import DiscountStrategy
from src.enums import StandardUnits
from src.constants import units_mapping
from src.utilities import extract_required_data


class ItemWiseDiscountStrategy(DiscountStrategy):
    """
    This is the item wise discount strategy class
    """

    def __init__(self, discount_str: str) -> None:
        """
        Initialization method for item wise discount class.

        Args:
            discount_str: discount string containing the discount in free items
        """

        # extract the two parts of the item wise discount string
        discount_criteria = discount_str.split('+')[0]
        discount_qnty = discount_str.split('+')[1]

        # find the items required to avail free items
        self.discount_criteria = self._find_discount_unit_wise(discount_str=discount_criteria)

        # find the free items that can availed
        self.discount_qnty = self._find_discount_unit_wise(discount_str=discount_qnty)

    def _find_discount_unit_wise(self, discount_str: str) -> int:
        """
        Finds the discount on the basis of given unit.

        Args:
            discount_str: discount str

        Returns:
            discount on the basis of unit
        """

        # fetch unit and discount
        unit = extract_required_data(data_str=discount_str, req_type=r'[a-zA-Z]+')
        discount = int(extract_required_data(data_str=discount_str, req_type=r'\d+'))

        # if a standard unit, return the same unit and price
        if StandardUnits.has_value(unit):
            return discount

        # if not a standard unit, convert the unit and discount
        discount *= units_mapping[unit]['std_equivalent_val']

        # return the new discount unit wise
        return discount