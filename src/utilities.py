#   Primary Author: Rahul Singh <rahulrsk07@gmail.com>
#
#   Purpose: This file contains basic utility functions used in our project

import re

from typing import Any


def extract_required_data(data_str: str, req_type: str) -> Any:
    """
    Extract the required data from a data string. Return None if not found.

    Args:
        data_str: string from which digits are to be extracted
        req_type: type of data to be extracted

    Returns:
        If found return it, else None

    """

    # try to find the required type of data
    digit_data = re.findall(req_type, data_str)

    if not digit_data:
        return None

    return digit_data[0]
