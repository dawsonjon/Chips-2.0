__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2012, Jonathan P Dawson"
__version__ = "0.1"

import os

class C2CHIPError(Exception):
    def __init__(self, message, filename=None, lineno=None):
        self.message = message
        self.filename = os.path.abspath(filename)
        self.lineno = lineno
