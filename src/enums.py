#   Primary Author: Rahul Singh <rahulrsk07@gmail.com>
#
#   Purpose: This file contains basic Enum classes

import enum


class StandardUnits(enum.Enum):
    """ This class contains Enum for Standard units"""
    Kilograms = 'kg'
    Litres = 'lt'

    @classmethod
    def has_value(cls, value: enum) -> enum:
        """
        Checks if a value is present in the current Enum class.

        Args:
            value: value to be checked

        Returns:
            True if present, else False
        """

        return value in cls._value2member_map_
