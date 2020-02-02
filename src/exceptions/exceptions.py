#   Primary Author: Rahul Singh <rahulrsk07@gmail.com>
#
#   Purpose: This file containing exceptions


class ReadFileError(Exception):
    """ Raise this when input file could not be read. """


class EmptyManagerInput(Exception):
    """ Raise this when manager input file is empty. """
