#   Primary Author: Rahul Singh <rahulrsk07@gmail.com>
#
#   Purpose: This file contains base entity class and some basic abstract methods

from typing import Any
from abc import abstractmethod


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
