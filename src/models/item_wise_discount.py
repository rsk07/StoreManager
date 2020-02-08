#   Primary Author: Rahul Singh <rahulrsk07@gmail.com>
#
#   Purpose: This file contains the item wise discount class

from src.models.discount import DiscountStrategy
from src.enums import StandardUnits
from src.constants import units_mapping
from src.utilities import extract_required_data


class ItemWiseDiscountStrategy(DiscountStrategy):
    pass