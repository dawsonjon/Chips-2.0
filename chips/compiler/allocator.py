__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2012, Jonathan P Dawson"
__version__ = "0.1"


class Allocator:

    """
    Maintain a pool of registers, variables and arrays.
    Keep track of what they are used for.
    """

    def __init__(self, reuse):
        self.registers = []
        self.all_registers = {}
        self.memory_size = 0
        self.reuse = reuse
        self.memory_content = {}
        self.start = 0
        self.handle = 0
        self.input_names = {}
        self.output_names = {}

    def new_input(self, name):
        handle = self.handle
        self.handle += 1
        self.input_names[handle] = name
        return handle

    def new_output(self, name):
        handle = self.handle
        self.handle += 1
        self.output_names[handle] = name
        return handle

