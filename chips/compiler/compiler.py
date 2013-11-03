#!/usr/bin/env python
"""A C to Verilog compiler"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2013, Jonathan P Dawson"
__version__ = "0.1"

import sys
import os

from chips.compiler.parser import Parser
from chips.compiler.exceptions import C2CHIPError
from chips.compiler.optimizer import parallelise
from chips.compiler.tokens import Tokens
from chips.compiler.verilog import generate_CHIP

def comp(C_file, options=[]):

  reuse = "no_reuse" not in options
  initialize_memory = "no_initialize_memory" not in options

  try:
      #compile into CHIP
      parser = Parser(C_file, reuse, initialize_memory)
      process = parser.parse_process()
      name = process.main.name
      instructions = process.generate()
      if "no_concurrent" in options:
        frames = [[i] for i in instructions]
      else:
        frames = parallelise(instructions)
      output_file = name + ".v"
      output_file = open(output_file, "w")
      inputs, outputs = generate_CHIP(
              C_file, 
              name, 
              frames, 
              output_file, 
              parser.allocator.all_registers,
              parser.allocator.memory_size, 
              initialize_memory, 
              parser.allocator.memory_content)
      output_file.close()
  except C2CHIPError as err:
      print "Error in file:", err.filename, "at line:", err.lineno
      print err.message
      sys.exit(-1)


  return name, inputs, outputs, ""
