#   Primary Author: Rahul Singh <rahulrsk07@gmail.com>
#
#   Purpose: This file is used to run all the trivial function required to process the input data and generate a
# customer bill

from src.utilities import read_file
from src.store_manager.store_manager_runner import StoreManager
from src.exceptions.exceptions import EmptyCustomerInput, EmptyManagerInput


def run() -> None:
    """
    This method is used to run all the functions required to process the manager and customer input and then generate
    a customer bll.

    Returns:
        None
    """

    store = StoreManager()

    manager_data = read_file(file='manager_input.txt')

    if not manager_data:
        raise EmptyManagerInput

    # process and store the initialization data for all the provided entities
    store.process_manager_data(data=manager_data)

    customer_data = read_file(file='customer_input.txt')

    if not customer_data:
        raise EmptyCustomerInput

    # validate and store the items which are found in the store so that bill is generated only for them
    processed_data = store.process_customer_input(customer_data=customer_data)

    # calculate and generate the final bill
    store.generate_bill(processed_data=processed_data)


if __name__ == '__main__':
    # run all the required functions
    run()
