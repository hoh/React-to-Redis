"""
Helper for opening files in the same directory as a Python file.
"""

import os.path


class Here(object):
    """Get a function `open_here` that opens a file in the same directory
    as the Python file.
    Usage:
    >>> open_here = opener(__file__)
    >>> f = open_here('somefile.txt').read()
    """

    def __init__(self, python_file_path):
        self.path = python_file_path

    def open(self, path, mode='r'):
        return open(os.path.join(os.path.dirname(self.path), path), mode=mode)
