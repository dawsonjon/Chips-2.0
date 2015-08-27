__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2012, Jonathan P Dawson"
__version__ = "0.1"

import os

class C2CHIPError(Exception):
    def __init__(self, message, filename=None, lineno=None):
        self.message = message
        if filename is not None:
            self.filename = os.path.abspath(filename)
        else:
            self.filename = None
        self.lineno = lineno

class StopSim(Exception):

    """A process has terminated
    
    """

    pass

class BreakSim(Exception):

    """A breakpoint has been reached
    
    """

    pass

class NoProfile(Exception):

    """A function requires profiling information, but none is available
    
    """

    pass

class NotConstant(Exception):

    """This expression gets raised when a non-constant ...
    
    Expression is evaluated at compile time.

    """

    pass
