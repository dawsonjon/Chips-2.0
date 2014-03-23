__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2012, Jonathan P Dawson"
__version__ = "0.1"

class Allocator:

    """Maintain a pool of registers, variables and arrays. Keep track of what they are used for."""

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

    def input_name(self, handle):
        return self.input_names[handle]

    def output_name(self, handle):
        return self.output_names[handle]

    def freeze(self):
        self.start = max(self.all_registers.keys()) + 1

    def new_array(self, size, contents):
        reg = self.memory_size
        self.memory_size += int(size)
        if contents is not None:
            for location, value in enumerate(contents, reg):
                self.memory_content[location] = value
        return reg

    def regsize(self, reg):
        return self.all_registers[reg][1]

    def new(self, size, name="temporary_register"):
        reg = self.start
        while 1:
            space = True
            for i in range(size//4):
                if reg + i in self.registers:
                    space = False
            if space:
                break
            reg += 1
        for i in range(size//4):
            self.registers.append(reg + i)
            self.all_registers[reg + i] = (name, size)
        return reg

    def free(self, register):
        if register in self.registers and self.reuse:
            self.registers.remove(register)

