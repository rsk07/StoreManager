#   Primary Author: Rahul Singh <rahulrsk07@gmail.com>
#
#   Purpose: This file contains the Supermarket manager class. The class contains all the required functions to
# initialize the supermarket store and generate a bill for customer


from src.constants import CATEGORY, SUB_CATEGORY, ITEM
from src.models.category import Category
from src.models.sub_category import SubCategory
from src.models.item import Item


class SupermarketManager:
    """
    This class contains methods and attributes required to initialize entities of a supermarket store and generate
    bills for customers.
    """

    def __init__(self) -> None:
        """
        Initialization method for supermarket manager class.
        """

        # mapping for entities and its corresponding classes
        self.entities = {
            CATEGORY: Category,
            SUB_CATEGORY: SubCategory,
            ITEM: Item
        }

        # this mapping consists of entity types and all the new entities added within them. The new entities further
        # consists of new names mapped to their class's objects
        self.store_data = {
            CATEGORY: {},
            SUB_CATEGORY: {},
            ITEM: {}
        }

        # parent mapping for each entity
        self.parent_type_map = {
            SUB_CATEGORY: CATEGORY,
            ITEM: SUB_CATEGORY,
            CATEGORY: None
        }
