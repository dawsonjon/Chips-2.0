"""Generate a python model equivilent to the generated verilog"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2013, Jonathan P Dawson"
__version__ = "0.1"

from numpy import uint32
from numpy import int32
from numpy import uint64
from numpy import int64
import struct

debug = False

class StopSim(Exception):
    pass

def unique(l):

    """In the absence of set in older python implementations, make list values unique"""

    return dict(zip(l, l)).keys()

def calculate_jumps(instructions):

    """change symbolic labels into numeric addresses"""

    #calculate the values of jump locations
    location = 0
    labels = {}
    new_instructions = []
    for instruction in instructions:
       if instruction["op"] == "label":
            labels[instruction["label"]] = location
       else:
            new_instructions.append(instruction)
            location += 1
    instructions = new_instructions

    #substitue real values for labeled jump locations
    for instruction in instructions:
        if "label" in instruction:
            instruction["label"]=labels[instruction["label"]]

    return instructions


def generate_python_model(input_file,
                  name,
                  instructions,
                  registers,
                  allocator,
                  inputs,
                  outputs):

    instructions = calculate_jumps(instructions)

    input_files = unique([i["file_name"] for i in instructions if "file_read" == i["op"]])
    output_files = unique([i["file_name"] for i in instructions if i["op"] in ("file_write", "float_file_write", "long_float_file_write")])

    #map input numbers to port models
    numbered_inputs = {}
    for number, input_name in allocator.input_names.iteritems():
        numbered_inputs[number] = inputs[input_name]
    numbered_outputs = {}
    for number, output_name in allocator.output_names.iteritems():
        numbered_outputs[number] = outputs[output_name]

    return PythonModel(instructions, allocator.memory_content, input_files, output_files, numbered_inputs, numbered_outputs)


class PythonModel:

    """create a python model equivilent to the generated verilog"""

    def __init__(self, instructions, memory_content, input_files, output_files, inputs, outputs):
        self.instructions = instructions
        self.memory_content = memory_content

        self.input_file_names = input_files
        self.output_file_names = output_files
        self.inputs = inputs
        self.outputs = outputs

    def simulation_reset(self):

        """reset the python model"""

        self.program_counter = 0
        self.register_hi = 0
        self.register_hib = 0
        self.carry = 0
        self.registers = {}
        self.memory = self.memory_content
        self.address = 0
        self.write_state = "wait_ack"
        self.read_state = "wait_stb"
        
        self.input_files = {}
        for file_name in self.input_file_names:
            file_ = open(file_name)
            self.input_files[file_name] = file_

        self.output_files = {}
        for file_name in self.output_file_names:
            file_ = open(file_name, "w")
            self.output_files[file_name] = file_

    def simulation_step(self):

        """execute the python simuilation by one step"""


        instruction = self.instructions[self.program_counter]

        if debug:
            print "executing...", self.program_counter, instruction,
            print "registers:", self.registers

        if "src" in instruction:
            src = instruction["src"]

        if "srcb" in instruction:
            srcb = instruction["srcb"]

        if "dest" in instruction:
            dest = instruction["dest"]

        if "literal" in instruction:
            literal = instruction["literal"]

        if "label" in instruction:
            literal = instruction["label"]

        this_instruction = self.program_counter
        self.program_counter += 1

        if instruction["op"] == "nop":
            pass

        elif instruction["op"] == "literal":
           self.registers[dest] = int32(literal)

        elif instruction["op"] == "move":
           self.registers[dest] = int32(self.registers[src])

        elif instruction["op"] == "not":
           self.registers[dest] = int32(~self.registers[src])

        elif instruction["op"] == "int_to_float":
           f = float(self.registers[src])
           self.registers[dest] = int32(float_to_bits(f))

        elif instruction["op"] == "float_to_int":
           i = bits_to_float(self.registers[src])
           self.registers[dest] = int32(i)

        elif instruction["op"] == "long_to_double":
           double = float(join_words(self.register_hi, self.registers[src]))
           self.register_hi, self.registers[dest] = split_word(double_to_bits(double))

        elif instruction["op"] == "double_to_long":
           bits = int(bits_to_double(join_words(self.register_hi, self.registers[src])))
           self.register_hi, self.registers[dest] = split_word(bits)

        elif instruction["op"] == "float_to_double":
           f = bits_to_float(self.registers[src])
           bits = double_to_bits(f)
           self.register_hi, self.registers[dest] = split_word(bits)

        elif instruction["op"] == "double_to_float":
           f = bits_to_double(join_words(self.register_hi, self.registers[src]))
           bits = float_to_bits(f)
           self.registers[dest] = bits

        elif instruction["op"] == "load_hi":
           self.register_hi = int32(self.registers[src])
           self.registerb_hi = int32(self.registers[srcb])

        elif instruction["op"] == "add":
           lw = int(uint32(self.registers[src])) + int(uint32(self.registers[srcb]))
           self.carry, self.registers[dest] = split_word(lw)
           self.carry &= 1

        elif instruction["op"] == "add_with_carry":
           lw = int(uint32(self.registers[src])) + int(uint32(self.registers[srcb])) + self.carry
           self.carry, self.registers[dest] = split_word(lw)
           self.carry &= 1

        elif instruction["op"] == "subtract":
           lw = int(uint32(self.registers[src])) + ~int(uint32(self.registers[srcb])) + 1
           self.carry, self.registers[dest] = split_word(lw)
           self.carry &= 1
           self.carry ^= 1

        elif instruction["op"] == "subtract_with_carry":
           lw = int(uint32(self.registers[src])) + ~int(uint32(self.registers[srcb])) + self.carry
           self.carry, self.registers[dest] = split_word(lw)
           self.carry &= 1
           self.carry ^= 1

        elif instruction["op"] == "multiply":
           lw = int(uint32(self.registers[src])) * int(uint32(self.registers[srcb]))
           self.register_hi, self.registers[dest] = split_word(lw)

        elif instruction["op"] == "result_hi":
           self.registers[dest] = int32(self.register_hi)

        elif instruction["op"] == "or":
           self.registers[dest] = int32(
           uint32(self.registers[src]) | 
           uint32(self.registers[srcb]))

        elif instruction["op"] == "and":
           self.registers[dest] = int32(uint32(self.registers[src]) & uint32(self.registers[srcb]))

        elif instruction["op"] == "xor":
           self.registers[dest] = int32(uint32(self.registers[src]) ^ uint32(self.registers[srcb]))

        elif instruction["op"] == "shift_left":
           self.carry = (uint32(self.registers[src]) & 0x80000000) >> 31
           self.registers[dest] = uint32(self.registers[src] << 1)

        elif instruction["op"] == "shift_left_with_carry":
           carry_in = self.carry
           self.carry = (uint32(self.registers[src]) & 0x80000000) >> 31
           self.registers[dest] = uint32(self.registers[src] << 1) | carry_in

        elif instruction["op"] == "shift_right":
           self.registers[dest] = int32(self.registers[src]) >> 1
           self.carry = self.registers[src] & 1

        elif instruction["op"] == "unsigned_shift_right":
           self.registers[dest] = uint32(self.registers[src]) >> 1
           self.carry = self.registers[src] & 1

        elif instruction["op"] == "shift_right_with_carry":
           self.registers[dest] = (uint32(self.registers[src]) >> 1) | (self.carry << 31)
           self.carry = self.registers[src] & 1

        elif instruction["op"] == "greater":
           self.registers[dest] = int32(int32(self.registers[src]) > int32(self.registers[srcb]))

        elif instruction["op"] == "greater_equal":
           self.registers[dest] = int32(int32(self.registers[src]) >= int32(self.registers[srcb]))

        elif instruction["op"] == "unsigned_greater":
           self.registers[dest] = int32(uint32(self.registers[src]) > uint32(self.registers[srcb]))

        elif instruction["op"] == "unsigned_greater_equal":
           self.registers[dest] = int32(uint32(self.registers[src]) >= uint32(self.registers[srcb]))

        elif instruction["op"] == "equal":
           self.registers[dest] = int32(int32(self.registers[src]) == int32(self.registers[srcb]))

        elif instruction["op"] == "not_equal":
           self.registers[dest] = int32(int32(self.registers[src]) != int32(self.registers[srcb]))

        elif instruction["op"] == "float_add":
           float_ = bits_to_float(self.registers[src])
           floatb = bits_to_float(self.registers[srcb])
           result = float_ + floatb
           self.registers[dest] = float_to_bits(result)

        elif instruction["op"] == "float_subtract":
           float_ = bits_to_float(self.registers[src])
           floatb = bits_to_float(self.registers[srcb])
           result = float_ - floatb
           self.registers[dest] = float_to_bits(result)

        elif instruction["op"] == "float_multiply":
           float_ = bits_to_float(self.registers[src])
           floatb = bits_to_float(self.registers[srcb])
           result = float_ * floatb
           self.registers[dest] = float_to_bits(result)

        elif instruction["op"] == "float_divide":
           float_ = bits_to_float(self.registers[src])
           floatb = bits_to_float(self.registers[srcb])
           result = float_ / floatb
           self.registers[dest] = float_to_bits(result)

        elif instruction["op"] == "long_float_add":
           double = bits_to_double(join_words(self.register_hi, self.registers[src]))
           doubleb = bits_to_double(join_words(self.registerb_hi, self.registers[srcb]))
           result = double + doubleb
           self.register_hi, self.registers[dest] = split_word(double_to_bits(result))

        elif instruction["op"] == "long_float_subtract":
           double = bits_to_double(join_words(self.register_hi, self.registers[src]))
           doubleb = bits_to_double(join_words(self.registerb_hi, self.registers[srcb]))
           result = double - doubleb
           self.register_hi, self.registers[dest] = split_word(double_to_bits(result))

        elif instruction["op"] == "long_float_multiply":
           double = bits_to_double(join_words(self.register_hi, self.registers[src]))
           doubleb = bits_to_double(join_words(self.registerb_hi, self.registers[srcb]))
           result = double * doubleb
           self.register_hi, self.registers[dest] = split_word(double_to_bits(result))

        elif instruction["op"] == "long_float_divide":
           double = bits_to_double(join_words(self.register_hi, self.registers[src]))
           doubleb = bits_to_double(join_words(self.registerb_hi, self.registers[srcb]))
           result = double / doubleb
           self.register_hi, self.registers[dest] = split_word(double_to_bits(result))

        elif instruction["op"] == "jmp_if_false":
            if self.registers[src] == 0:
                self.program_counter = literal

        elif instruction["op"] == "jmp_if_true":
            if self.registers[src] != 0:
                self.program_counter = literal

        elif instruction["op"] == "jmp_and_link":
            self.registers[dest] = self.program_counter
            self.program_counter = literal

        elif instruction["op"] == "jmp_to_reg":
            self.program_counter = self.registers[src]

        elif instruction["op"] == "goto":
            self.program_counter = literal

        elif instruction["op"] == "file_read":
            value = self.input_files[instruction["filename"]].getline()
            self.registers[dest] = int32(value)

        elif instruction["op"] == "float_file_write":
            self.output_files[instruction["file_name"]].write("%f\n"%bits_to_float(self.registers[src]))

        elif instruction["op"] == "long_float_file_write":
            long_word = join_words(self.register_hi, self.registers[src])
            self.output_files[instruction["file_name"]].write("%f\n"%bits_to_double(long_word))

        elif instruction["op"] == "unsigned_file_write":
            self.output_files[instruction["file_name"]].write("%i\n"%uint32(self.registers[src]))

        elif instruction["op"] == "file_write":
            self.output_files[instruction["file_name"]].write("%i\n"%int32(self.registers[src]))

        elif instruction["op"] == "read":


            input_ = self.inputs[self.registers[src]]
            self.program_counter = this_instruction

            if self.read_state == "wait_stb":
                if input_.stb:
                    input_.ack = True
                    self.read_state = "wait_nstb"
                    self.registers[dest] = input_.data
            elif self.read_state == "wait_nstb":
                if not input_.stb:
                    input_.ack = False
                    self.read_state = "wait_stb"
                    self.program_counter += 1

        elif instruction["op"] == "ready":
            input_ = self.inputs[self.registers[src]]
            self.registers[dest] = int32(int(input_.stb))

        elif instruction["op"] == "write":

            output = self.outputs[self.registers[src]]
            output.data = self.registers[srcb]
            self.program_counter = this_instruction

            if self.write_state == "wait_ack":
                output.stb = True
                if output.ack:
                    output.stb = False
                    self.write_state = "wait_nack"
            elif self.write_state == "wait_nack":
                if not output.ack:
                    self.write_state = "wait_ack"
                    self.program_counter += 1

        elif instruction["op"] == "memory_read":
            self.address = self.registers[src]
            self.registers[dest] = int32(self.memory[self.address])

        elif instruction["op"] == "memory_write":
            self.memory[self.registers[src]] = int32(self.registers[srcb])

        elif instruction["op"] == "assert":
            if self.registers[src] == 0:
                print "Assertion failed at line: %s in file: %s"%(
                  instruction["line"],
                  instruction["file"],
                )
                exit(1)

        elif instruction["op"] == "wait_clocks":
            pass

        elif instruction["op"] == "report":
            print "%d (report at line: %s in file: %s)"%(
                self.registers[src],
                instruction["line"],
                instruction["file"],
            )

        elif instruction["op"] == "long_report":
            print "%d (report at line: %s in file: %s)"%(
                join_words(self.register_hi, self.registers[src]),
                instruction["line"],
                instruction["file"],
            )

        elif instruction["op"] == "float_report":
            print "%f (report at line: %s in file: %s)"%(
                bits_to_float(self.registers[src]),
                instruction["line"],
                instruction["file"],
            )

        elif instruction["op"] == "long_float_report":
            print "%f (report at line: %s in file: %s)"%(
                bits_to_double(join_words(self.register_hi, self.registers[src])),
                instruction["line"],
                instruction["file"],
            )

        elif instruction["op"] == "unsigned_report":
            print "%d (report at line: %s in file: %s)"%(
                uint32(self.registers[src]),
                instruction["line"],
                instruction["file"],
            )

        elif instruction["op"] == "long_unsigned_report":
            print "%d (report at line: %s in file: %s)"%(
                uint64(join_words(self.register_hi, self.registers[src])),
                instruction["line"],
                instruction["file"],
            )

        elif instruction["op"] == "stop":
            self.program_counter = this_instruction
            for file_ in self.input_files.values():
                file_.close()
            for file_ in self.output_files.values():
                file_.close()
            raise StopSim

def float_to_bits(f):
    
    "convert a floating point number into an integer containing the ieee 754 representation."

    value = 0
    for byte in struct.pack(">f", f):
         value <<= 8
         value |= ord(byte)
    return int32(value)

def double_to_bits(f):

    "convert a double precision floating point number into a 64 bit integer containing the ieee 754 representation."

    value = 0
    for byte in struct.pack(">d", f):
         value <<= 8
         value |= ord(byte) 
    return uint64(value)

def bits_to_float(bits):

    "convert integer containing the ieee 754 representation into a float"

    byte_string = (
        chr((bits & 0xff000000) >> 24) +
        chr((bits & 0xff0000) >> 16) +
        chr((bits & 0xff00) >> 8) +
        chr((bits & 0xff))
    )
    return struct.unpack(">f", byte_string)[0]

def bits_to_double(bits):

    "convert integer containing the ieee 754 representation into a float"

    bits = int(bits)
    byte_string = (
        chr((bits & 0xff00000000000000) >> 56) +
        chr((bits & 0xff000000000000) >> 48) +
        chr((bits & 0xff0000000000) >> 40) +
        chr((bits & 0xff00000000) >> 32) +
        chr((bits & 0xff000000) >> 24) +
        chr((bits & 0xff0000) >> 16) +
        chr((bits & 0xff00) >> 8) +
        chr((bits & 0xff))
    )
    return struct.unpack(">d", byte_string)[0]

def join_words(hi, lo):

    """join two 32 bit words into a 64 bit word"""

    return int64((int(hi) << 32) | (int(lo) & 0xffffffff))

def split_word(lw):

    """split a 64 bit words into two 32 bit words"""

    return int32(int(lw) >> 32), int32(int(lw) & 0xffffffff)
