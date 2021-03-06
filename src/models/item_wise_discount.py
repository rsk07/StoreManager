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

    @staticmethod
    def validate(discount_str: str) -> bool:
        """
        Validates the discount string.

        Args:
            discount_str:

        Returns:
            True if valid, else False
        """

        # fetch the first and second part of the discount string
        # first part - contains the items required to satisfy the discount criteria
        # second part - contains free items that can be availed with that criteria
        discount_data = discount_str.split('+')
        discount_criteria = discount_data[0]
        discount_qnty = discount_data[1]

        return ItemWiseDiscountStrategy.validate_digits(part_a=discount_criteria,
                                                        part_b=discount_qnty) and \
               ItemWiseDiscountStrategy.validate_units(part_a=discount_criteria,
                                                       part_b=discount_qnty)

    @staticmethod
    def validate_digits(part_a: str, part_b: str) -> bool:
        """
        Validate the digits in the given data.

        Args:
            part_a: first part
            part_b: second part

        Returns:
            True if valid, else False
        """

        # return false if no digit found in either part
        if not extract_required_data(part_a, req_type=r'[a-zA-Z]+') or not extract_required_data(part_b,
                                                                                                 req_type=r'[a-zA-Z]+'):
            return False

        return True

    @staticmethod
    def validate_units(part_a: str, part_b: str) -> bool:
        """
        Validate the unit strings in the given data.

        Args:
            part_a: first part
            part_b: second part

        Returns:
            True if valid, else False
        """

        # fetch the units str from both the parts
        criteria_unit = extract_required_data(part_a, req_type=r'\D+')
        qnty_unit = extract_required_data(part_b, req_type=r'\D+')

        # if no units data found
        if not criteria_unit or not qnty_unit:
            return False

        if criteria_unit not in units_mapping and not StandardUnits.has_value(criteria_unit):
            return False

        if qnty_unit not in units_mapping and not StandardUnits.has_value(qnty_unit):
            return False

        return True

    def get_discount(self, quantity: int, price_per_unit: int) -> None:
        """
        Calculate and returns the applicable discount.

        Returns:
            None
        """
        # total items required to get some free items
        criteria_qnty = self.discount_criteria

        # total free items to be given
        discount_qnty = self.discount_qnty

        qnty_left = quantity

        # stores total free items that can be availed
        free_item_count = 0

        # find out total free items that can be availed
        while qnty_left > criteria_qnty:
            diff = qnty_left - criteria_qnty
            curr_free_items = min(diff, discount_qnty)
            free_item_count += curr_free_items
            qnty_left -= (curr_free_items + criteria_qnty)

        # calculate the price for free items
        discount = free_item_count * price_per_unit

        return discount
