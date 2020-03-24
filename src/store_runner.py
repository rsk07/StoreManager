#   Primary Author: Rahul Singh <rahulrsk07@gmail.com>
#
#   Purpose: This file is used to run all the trivial function required to process the input data and generate a
# customer bill

from src.utilities import read_file
from src.store_manager.store_manager_runner import SupermarketManager


def run() -> None:
    """
    This method is used to run all the functions required to process the manager and customer input and then generate
    a customer bll.

    Returns:
        None
    """

    store = SupermarketManager()

    manager_data = read_file(file='manager_input.txt')