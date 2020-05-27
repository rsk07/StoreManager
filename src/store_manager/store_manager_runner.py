#   Primary Author: Rahul Singh <rahulrsk07@gmail.com>
#
#   Purpose: This file contains the Supermarket manager class. The class contains all the required functions to
# initialize the supermarket store and generate a bill for customer

from typing import Any
from traceback import format_exc

from src.constants import units_mapping
from src.models.entity import Entity
from src.constants import CATEGORY, SUB_CATEGORY, ITEM
from src.models.category import Category
from src.models.sub_category import SubCategory
from src.models.item import Item
from src.models.percentage_wise_discount import PercentageWiseDiscountStrategy
from src.utilities import extract_required_data
from src.exceptions.exceptions import CustomerInputProcessingError, BillGenerationError


class StoreManager:
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

    def _validate_entity_parent(self, entity_parent_name: str, entity_parent_type: str) -> bool:
        """
        Checks if parent entity name is present in its corresponding entity type.

        Args:
            entity_parent_name: entity name to be checked
            entity_parent_type: entity type where we need to check the name

        Returns:
            True, if found, else False
        """

        # for Category entity
        if not entity_parent_type:
            return True

        # check if parent is found
        return entity_parent_name in self.store_data[entity_parent_type]

    def _store_entity_mapping(self, entity_type: str, entity_obj: Entity) -> None:
        """
        Store the entity mapping in its corresponding entity type.

        Args:
            entity_type: entity type where we need to add the mapping
            entity_obj: entity object which is to be added

        Returns:
            None
        """

        self.store_data[entity_type][entity_obj.name] = entity_obj

    def process_customer_input(self, customer_data: str) -> list:
        """
        Process and validate the input data for items provided by the customer.

        Args:
            customer_data: customer data to be processed

        Returns:
            list of items for which bill is to be generated
        """

        try:
            # split the items by a comma
            all_items_data = customer_data.split(',')
            # strip extra spaces and convert the data to lower case
            all_items_data = [(val.strip()).lower() for val in all_items_data]

            # process the data for all the input items and stores the ones which are valid
            processed_data = self._process_item_data(all_items_data=all_items_data)

        except Exception as e:
            print(f"Failed to generate bill as customer input cannot be processed.Exception: {e}\nTraceback: "
                  f"{format_exc()}")
            raise CustomerInputProcessingError

        # list of valid items for which bill is to be generated
        return processed_data

    def _process_item_data(self, all_items_data: list) -> list:
        """
        Process the data for all the input items and store the ones which are valid

        Args:
            all_items_data: list of all the input items

        Returns:
            list of valid items for which bill is to be generated
        """

        # list to store the valid data for which bill needs to be generated
        processed_data = []

        for item_data in all_items_data:
            # arguments must contain item name and quantity
            item_data = item_data.split(' ')
            if len(item_data) < 2:
                print('Invalid number of item arguments')
                continue

            # if len of arguments is greater than 2, take the last argument as quantity and rest as item name
            item_name = item_data[0]
            item_qnty_data = item_data[-1]

            if len(item_data) > 2:
                item_name = ' '.join(item_data[:-1])

            # try to fetch the item's object from its corresponding entity type mapping
            item_obj = self.store_data[ITEM].get(item_name)

            # ignore the input if item not found
            if not item_obj:
                print(f'Sorry, the item {item_name} was not found')
                continue

            # check if quantity contains a digit
            item_qnty_digit = float(
                    extract_required_data(data_str=item_qnty_data, req_type=r'[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)')[0])

            # if no digit found, ignore the current item
            if not item_qnty_digit:
                print(f'Please specify the quantity in number for the item {item_name}')
                continue

            # find the unit
            item_qnty_unit = self._find_item_unit(item_qnty_data=item_qnty_data, item_name=item_name, item_obj=item_obj)

            if not item_qnty_unit:
                continue

            # if unit not a standard one, convert it and modify the item_quantity accordingly
            if item_qnty_unit in units_mapping:
                item_qnty_digit *= units_mapping[item_qnty_unit]['std_equivalent_val']
                item_qnty_unit = units_mapping[item_qnty_unit]['std_equivalent_unit']

            # store the item data for which bill needs to be generated
            processed_data.append(
                    {
                        'item': item_obj,
                        'quantity': item_qnty_digit,
                        'unit': item_qnty_unit
                    }
            )

        # return the processed data
        return processed_data

    def _find_item_unit(self, item_qnty_data: str, item_name: str, item_obj: Item) -> Any:
        """
        Validates unit in the given string.

        Args:
            item_qnty_data: quantity data in which contains the unit
            item_name: name of the current item

        Returns:
            item's quantity and standard unit
        """

        # check if quantity contains unit
        item_qnty_unit = extract_required_data(data_str=item_qnty_data, req_type=r'[a-zA-Z]+')
        # if no unit characters found, return None
        if not item_qnty_unit:
            print(f'Please specify the quantity for the item {item_name}')
            return None

        # if unit matches item's std unit
        if item_qnty_unit == item_obj.unit:
            return item_qnty_unit

        # if unit not found in the stored units, return None
        if item_qnty_unit not in units_mapping:
            print(f'Please add a valid unit for the item {item_name}')
            return None

        # if unit's equivalent std unit doesn't matches item's std unit
        if units_mapping[item_qnty_unit]['std_equivalent_unit'] != item_obj.unit:
            print(f'Please add a valid unit for the item {item_name}')
            return None

        return item_qnty_unit

    @staticmethod
    def generate_bill(processed_data: dict) -> None:
        """
        Calculate the total cost of items after applying discount and generate the bill.

        Args:
            processed_data: list of valid data for which bill needs to be generated

        Returns:
            None
        """

        # stores total original cost without discount
        total_original_cost = 0.0
        # stores total original cost with discount
        total_new_cost = 0.0

        print("\n\n=================================================")
        print("HERE's YOUR BILL, HAVE A NICE DAY!")
        print("=================================================")

        # process all the items
        for data in processed_data:
            try:
                # calculate the total cost for current item and add it to the overall cost
                original_cost = round(data['item'].get_price(quantity=data['quantity']), 2)
                total_original_cost += original_cost

                # get total discount
                if isinstance(data['item'].discount_strategy, PercentageWiseDiscountStrategy):
                    discount = data['item'].get_discount(original_cost, data['item'].get_max_discount())
                else:
                    discount = data['item'].get_discount(data['quantity'], data['item'].price_per_unit)

                # add the new cost for current item
                new_cost = round(original_cost - discount, 2)

                # update the total new cost
                total_new_cost += new_cost

                print(f"{data['item'].name} -> {data['quantity']}{data['unit']} -> Rs {new_cost}")

            except Exception as e:
                print(f"Data {data} is invalid. Ignoring this item. Exception: {e}\nTraceback: "
                      f"{format_exc()}")
                raise BillGenerationError

        # print the billing details
        print("=================================================")
        print(f"Total Amount: Rs {total_new_cost}")
        print(f"You saved: {total_original_cost} - {total_new_cost} = Rs {total_original_cost-total_new_cost}")
        print("=================================================")
