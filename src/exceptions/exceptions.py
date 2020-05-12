#   Primary Author: Rahul Singh <rahulrsk07@gmail.com>
#
#   Purpose: This file containing exceptions


class ReadFileError(Exception):
    """ Raise this when input file could not be read. """


class EmptyManagerInput(Exception):
    """ Raise this when manager input file is empty. """

class EmptyCustomerInput(Exception):
    """ Raise this when customer input file is empty. """

class CustomerInputProcessingError(Exception):
    """ Raise this when input provided by the customer could not be processed. """