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

    def process_manager_data(self, data: str) -> None:
        """
        Processes manager data (initialize supermarket's data) and check for basic validations.

        Args:
            data: the data to be processed

        Returns:
            None
        """

        # split the data line wise
        line_wise_data = data.split('\n')

        # store data for each line
        for line_data in line_wise_data:
            # ignore empty lines
            if not line_data:
                continue

            try:
                # split the line, remove any extra spaces and convert all the values into lower case
                entity_type = ((line_data.split(',')[0]).strip()).lower()

                # first argument is the entity type ( For E.g: For Dairy, entity type is 'Category'
                args = line_data.split(',')[1:]

                # first argument of the remaining arguments is the name of parent entity
                entity_parent_name = ((args[0]).strip()).lower()

                # if current customer data is invalid, ignore the data
                if not self._validate_curr_customer_data(entity_type=entity_type,
                                                         entity_parent_name=entity_parent_name):
                    continue

                # strip and convert all the other arguments to lower case
                args = [(val.strip()).lower() for val in args]

                # store the entity data after checking for its corresponding entity specific validations
                self._store_entity_data(entity_type=entity_type, args=args)

            except Exception as e:
                print(f"Line data {line_data} is invalid. Ignoring this line. Exception: {e}\nTraceback: "
                      f"{format_exc()}")

    def _validate_curr_customer_data(self, entity_type: str, entity_parent_name: str) -> bool:
        """
        Checks the validations for the current customer data.

        Args:
            entity_type: entity type of the data
            entity_parent_name: entity's parent name

        Returns:
            True is valid, else False
        """

        # check if entity type is valid
        if entity_type not in self.entities:
            print(f"Entity type {entity_type} not found entities. Ignoring the current input line.")
            return False

        # check if parent entity name has been added
        if not self._validate_entity_parent(entity_parent_name=entity_parent_name,
                                            entity_parent_type=self.parent_type_map[entity_type]):
            print(f"Parent entity {entity_parent_name} not found in {self.parent_type_map[entity_type]}. "
                  f"Ignoring the current input line.")
            return False

        return True

    def _store_entity_data(self, entity_type: str, args: Any) -> Any:
        """
        Check for entity specific validations and store the newly created entiyy object.

        Args:
            entity_type: Entity type
            args: arguments to be stored for the current entity

        Returns:
            None
        """

        if not self.entities[entity_type].validate_args(*args):
            return None

        # if entity has a parent
        if self.parent_type_map[entity_type]:
            parent_entity_name = args[0]
            # store the parent object for current entity name instead of the parent name
            args[0] = self.store_data[self.parent_type_map[entity_type]][parent_entity_name]

        # create the entity object and store it in its corresponding entity type
        entity_obj = self.entities[entity_type](*args)
        self._store_entity_mapping(entity_type=entity_type, entity_obj=entity_obj)
