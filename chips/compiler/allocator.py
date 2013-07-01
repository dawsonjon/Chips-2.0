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

  def new_array(self, size):
    reg = self.memory_size
    self.memory_size += int(size)
    return reg

  def new(self, name="temporary_register"):
    reg = 0
    while reg in self.registers:
      reg += 1
    self.registers.append(reg)
    self.all_registers[reg] = name
    return reg

  def free(self, register):
    if register in self.registers and self.reuse:
      self.registers.remove(register)
