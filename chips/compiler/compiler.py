#!/usr/bin/env python
"""A C to Verilog compiler"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2013, Jonathan P Dawson"
__version__ = "0.1"

import sys
import os

from chips.compiler.parser import Parser
from chips.compiler.exceptions import C2CHIPError
from chips.compiler.optimizer import cleanup_functions
from chips.compiler.macro_expander import expand_macros
from chips.compiler.tokens import Tokens
from chips.compiler.verilog_area import generate_CHIP as generate_CHIP_area
from chips.compiler.python_model import generate_python_model
from chips.api.hash import dict_to_hash
import fpu

def generate_library():
    output_file = open("chips_lib.v", "w")
    output_file.write(fpu.adder)
    output_file.write(fpu.divider)
    output_file.write(fpu.multiplier)
    output_file.write(fpu.double_divider)
    output_file.write(fpu.double_multiplier)
    output_file.write(fpu.double_adder)
    output_file.write(fpu.int_to_float)
    output_file.write(fpu.float_to_int)
    output_file.write(fpu.long_to_double)
    output_file.write(fpu.double_to_long)
    output_file.write(fpu.float_to_double)
    output_file.write(fpu.double_to_float)
    output_file.close()

def comp(input_file, options=[], parameters={}):

    reuse = "no_reuse" not in options
    initialize_memory = "no_initialize_memory" not in options
    generate_library()

    try:
            #Optimize for area
            parser = Parser(input_file, reuse, initialize_memory, parameters)
            process = parser.parse_process()
            name = process.main.name + dict_to_hash(parameters)
            instructions = process.generate()
            if "dump_raw" in options:
                for i in instructions:
                    print i
            instructions = expand_macros(instructions, parser.allocator)
            instructions = cleanup_functions(instructions)
            instructions, registers = cleanup_registers(instructions, parser.allocator.all_registers)
            if "dump_optimised" in options:
                for i in instructions:
                    print i
            output_file = name + ".v"
            output_file = open(output_file, "w")
            inputs, outputs = generate_CHIP_area(
                    input_file,
                    name,
                    instructions,
                    output_file,
                    registers,
                    parser.allocator,
                    initialize_memory)
            output_file.close()

    except C2CHIPError as err:
        print "Error in file:", err.filename, "at line:", err.lineno
        print err.message
        sys.exit(-1)


    return name, inputs, outputs, ""

def compile_python_model(
        input_file, 
        options=[], 
        parameters = {}, 
        inputs = {}, 
        outputs = {}
        ):

    reuse = "no_reuse" not in options
    initialize_memory = "no_initialize_memory" not in options
    generate_library()

    try:
            #Optimize for area
            parser = Parser(input_file, reuse, initialize_memory, parameters)
            process = parser.parse_process()
            name = process.main.name + dict_to_hash(parameters)
            instructions = process.generate()
            if "dump" in options:
                for i in instructions:
                    print i
            instructions = expand_macros(instructions, parser.allocator)

            model = generate_python_model(
                    input_file,
                    name,
                    instructions,
                    parser.allocator, 
                    inputs, 
                    outputs)

            return model, parser.allocator.input_names.values(), parser.allocator.output_names.values(), name

    except C2CHIPError as err:
        print "Error in file:", err.filename, "at line:", err.lineno
        print err.message
        sys.exit(-1)

