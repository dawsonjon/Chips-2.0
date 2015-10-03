"""Generate a python model equivalent to the generated verilog"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2013, Jonathan P Dawson"
__version__ = "0.1"

from numpy import uint32
from numpy import int32
from numpy import uint64
from numpy import int64
import sys
import math
import register_map
from chips.compiler.exceptions import StopSim, BreakSim, ChipsAssertionFail
from utils import unique, calculate_jumps, bits_to_double, double_to_bits
from utils import bits_to_float, float_to_bits, split_word, join_words

def generate_python_model(
        debug,
        input_file,
        name,
        instructions,
        allocator,
        inputs,
        outputs,
        profile = False
    ):

    instructions = calculate_jumps(instructions)

    input_files = unique([i["file_name"] for i in instructions if "file_read" == i["op"]])
    output_files = unique([i["file_name"] for i in instructions if i["op"].endswith("file_write")])

    #map input numbers to port models
    numbered_inputs = {}
    for number, input_name in allocator.input_names.iteritems():
        if input_name in inputs:
            numbered_inputs[number] = inputs[input_name]
    numbered_outputs = {}
    for number, output_name in allocator.output_names.iteritems():
        if output_name in outputs:
            numbered_outputs[number] = outputs[output_name]

    return PythonModel(
        debug,
        instructions, 
        allocator.memory_content, 
        input_files, 
        output_files, 
        numbered_inputs, 
        numbered_outputs,
        profile,
    )


class PythonModel:

    """create a python model equivalent to the generated verilog"""

    def __init__(
            self, 
            debug,
            instructions, 
            memory_content, 
            input_files, 
            output_files, 
            inputs, outputs,
            profile = False
        ):
        self.debug = debug
        self.profile = profile
        self.instructions = instructions
        self.memory_content = memory_content

        self.input_file_names = input_files
        self.output_file_names = output_files
        self.inputs = inputs
        self.outputs = outputs

        self.breakpoints = {}

    def simulation_reset(self):

        """reset the python model"""

        self.program_counter = 0
        self.register_hi = 0
        self.register_hib = 0
        self.carry = 0
        self.memory = self.memory_content
        self.registers = {}
        self.address = 0
        self.write_state = "wait_ack"
        self.read_state = "wait_stb"
        self.a_lo = 0
        self.b_lo = 0
        self.a_hi = 0
        self.b_hi = 0
        self.max_stack = 0
        self.timer = 0


        self.files = {}
        
        self.input_files = {}
        for file_name in self.input_file_names:
            file_ = open(file_name)
            self.input_files[file_name] = file_

        self.output_files = {}
        for file_name in self.output_file_names:
            file_ = open(file_name, "w")
            self.output_files[file_name] = file_

    def get_line(self):
        trace = self.instructions[self.program_counter]["trace"]
        return trace.lineno

    def get_file(self):
        trace = self.instructions[self.program_counter]["trace"]
        return trace.filename

    def get_profile(self):
        if not self.profile:
            raise NoProfile
        return self.files

    def get_registers(self):
        return self.registers

    def get_memory(self):
        return self.memory

    def get_instruction(self):
        return self.instructions[self.program_counter]

    def get_program_counter(self):
        return self.program_counter

    def set_breakpoint(self, f, l):
        lines = self.breakpoints.get(f, {})
        lines[l] = True
        self.breakpoints[f] = lines

    def clear_breakpoint(self, f, l):
        lines = self.breakpoints.get(f, {})
        lines.pop(l)
        self.breakpoints[f] = lines

    def step_into(self):

        """run until a different line (e.g jump into functions)"""

        l = self.get_line()
        f = self.get_file()
        while(l == self.get_line() and f == self.get_file()):
            self.simulation_step()

    def step_over(self):

        """run until the next line (e.g. skip over functions)"""

        l = self.get_line()
        f = self.get_file()
        while(self.get_line() <= l and self.get_file != f):
            self.simulation_step()

    def simulation_step(self):

        """execute the python simulation by one step"""


        l = self.get_line()
        f = self.get_file()
        if f in self.breakpoints:
            if l in self.breakpoints[f]:
                raise BreakSim

        instruction = self.instructions[self.program_counter]
        current_stack = self.registers.get(register_map.tos, 0)
        self.max_stack = max([current_stack, self.max_stack])

        if self.profile:
            trace = instruction.get("trace", "-")
            lines = self.files.get(trace.filename, {})
            lines[trace.lineno] = lines.get(trace.lineno, 0) + 1
            self.files[trace.filename] = lines

        if "literal" in instruction:
            literal = instruction["literal"]

        if "label" in instruction:
            literal = instruction["label"]

        #read operands
        #
        a = instruction.get("a", 0)
        b = instruction.get("b", 0)
        z = instruction.get("z", 0)

        operand_b = self.registers.get(b, 0) 
        operand_a = self.registers.get(a, 0)

        this_instruction = self.program_counter
        self.program_counter += 1
        wait = False
        result = None

        if instruction["op"] == "stop":
            self.program_counter = this_instruction
            wait = True
            for file_ in self.input_files.values():
                file_.close()
            for file_ in self.output_files.values():
                file_.close()
            raise StopSim

        elif instruction["op"] == "literal":
           if literal & 0x8000:
               result = 0xffff0000 | literal
           else:
               result = literal
        elif instruction["op"] == "addl":
           result = literal+operand_a
        elif instruction["op"] == "literal_hi":
           result = operand_a & 0x0000ffff | ((literal & 0xffff) << 16)
        elif instruction["op"] == "store":
           self.memory[operand_a] = operand_b
        elif instruction["op"] == "load":
           result = self.memory.get(operand_a, 0)
        elif instruction["op"] == "call":
           result = this_instruction + 1
           self.program_counter = literal
        elif instruction["op"] == "return":
           self.program_counter = operand_a
        elif instruction["op"] == "a_lo":
           result = self.a_lo
           self.a_lo=operand_a
        elif instruction["op"] == "b_lo":
           result = self.b_lo
           self.b_lo=operand_a
        elif instruction["op"] == "a_hi":
           result = self.a_hi
           self.a_hi=operand_a
        elif instruction["op"] == "b_hi":
           result = self.b_hi
           self.b_hi=operand_a
        elif instruction["op"] == "not":
           result = uint32(~operand_a)
        elif instruction["op"] == "int_to_long":
           if operand_a & 0x80000000:
               result = uint32(0xffffffff)
           else:
               result = uint32(0x00000000)
        elif instruction["op"] == "int_to_float":
           f = float(int32(self.a_lo))
           print f
           self.a_lo = float_to_bits(f)
        elif instruction["op"] == "float_to_int":
           i = bits_to_float(self.a_lo)
           if math.isnan(i):
               self.a_lo = int32(0)
           else:
               self.a_lo = int32(i)
        elif instruction["op"] == "long_to_double":
           double = float(int64(join_words(self.a_hi, self.a_lo)))
           if math.isnan(double):
               self.a_hi, self.a_lo = split_word(0, 0)
           else:
               self.a_hi, self.a_lo = split_word(double_to_bits(double))
        elif instruction["op"] == "double_to_long":
           bits = int(bits_to_double(join_words(self.a_hi, self.a_lo)))
           self.a_hi, self.a_lo = split_word(bits)
        elif instruction["op"] == "float_to_double":
           f = bits_to_float(self.a_lo)
           bits = double_to_bits(f)
           self.a_hi, self.a_lo = split_word(bits)
        elif instruction["op"] == "double_to_float":
           f = bits_to_double(join_words(self.a_hi, self.a_lo))
           self.a_lo = float_to_bits(f)
        elif instruction["op"] == "add":
           a = operand_a
           b = operand_b
           lw = int(uint32(a)) + int(uint32(b))
           self.carry, result = split_word(lw)
           self.carry &= 1
        elif instruction["op"] == "add_with_carry":
           a = operand_a
           b = operand_b
           lw = int(uint32(a)) + int(uint32(b)) + self.carry
           self.carry, result = split_word(lw)
           self.carry &= 1
        elif instruction["op"] == "subtract":
           a = operand_a
           b = operand_b
           lw = int(uint32(a)) + ~int(uint32(b)) + 1
           self.carry, result = split_word(lw)
           self.carry &= 1
           self.carry ^= 1
        elif instruction["op"] == "subtract_with_carry":
           a = operand_a
           b = operand_b
           lw = int(uint32(a)) + ~int(uint32(b)) + self.carry
           self.carry, result = split_word(lw)
           self.carry &= 1
           self.carry ^= 1
        elif instruction["op"] == "multiply":
           a = operand_a
           b = operand_b
           lw = int(uint32(a)) * int(uint32(b))
           self.carry, result = split_word(lw)
        elif instruction["op"] == "carry":
           a = operand_a
           b = operand_b
           result = uint32(self.carry)
        elif instruction["op"] == "or":
           a = operand_a
           b = operand_b
           result = uint32(a | b)
        elif instruction["op"] == "and":
           a = operand_a
           b = operand_b
           result = uint32(a & b)
        elif instruction["op"] == "xor":
           a = operand_a
           b = operand_b
           result = uint32(a ^ b)
        elif instruction["op"] == "shift_left":
           a = operand_a
           b = int(operand_b)
           b = b if b <= 32 else 32
           self.carry = uint32(a) >> (32 - uint32(b))
           if b == 32:
               result = uint32(0)
           else:
               result = uint32(a) << uint32(b)
        elif instruction["op"] == "shift_left_with_carry":
           a = operand_a
           b = int(operand_b)
           b = b if b <= 32 else 32
           carry_in = self.carry
           self.carry = uint32(a) >> (32 - uint32(b))
           if b == 32:
               result = uint32(0) | carry_in
           else:
               result = uint32(a) << uint32(b) | carry_in
        elif instruction["op"] == "shift_right":
           a = operand_a
           b = int(operand_b)
           b = b if b <= 32 else 32
           self.carry = uint32(a) << (32 - uint32(b))
           result = uint32(int32(a) >> uint32(b))
        elif instruction["op"] == "unsigned_shift_right":
           a = operand_a
           b = int(operand_b)
           b = b if b <= 32 else 32
           self.carry = uint32(a) << (32 - uint32(b))
           if b == 32:
               result = uint32(0)
           else:
               result = uint32(a) >> uint32(b)
        elif instruction["op"] == "shift_right_with_carry":
           a = operand_a
           b = int(operand_b)
           b = b if b <= 32 else 32
           carry_in = self.carry
           self.carry = uint32(a) << (32 - uint32(b))
           if b == 32:
               result = uint32(0) | carry_in
           else:
               result = uint32(a) >> uint32(b) | carry_in
        elif instruction["op"] == "greater":
           a = operand_a
           b = operand_b
           result = int32(int32(a) > int32(b))
        elif instruction["op"] == "greater_equal":
           a = operand_a
           b = operand_b
           result = int32(int32(a) >= int32(b))
        elif instruction["op"] == "unsigned_greater":
           a = operand_a
           b = operand_b
           result = int32(uint32(a) > uint32(b))
        elif instruction["op"] == "unsigned_greater_equal":
           a = operand_a
           b = operand_b
           result = int32(uint32(a) >= uint32(b))
        elif instruction["op"] == "equal":
           a = operand_a
           b = operand_b
           result = int32(int32(a) == int32(b))
        elif instruction["op"] == "not_equal":
           a = operand_a
           b = operand_b
           result = int32(int32(a) != int32(b))
        elif instruction["op"] == "jmp_if_false":
            if operand_a == 0:
                self.program_counter = literal
        elif instruction["op"] == "jmp_if_true":
            if operand_a != 0:
                self.program_counter = literal
        elif instruction["op"] == "goto":
            self.program_counter = literal
        elif instruction["op"] == "file_read":
            value = self.input_files[instruction["filename"]].getline()
            result = uint32(value)
        elif instruction["op"] == "float_file_write":
            self.output_files[instruction["file_name"]].write("%.7f\n"%bits_to_float(operand_a))
        elif instruction["op"] == "unsigned_file_write":
            self.output_files[instruction["file_name"]].write("%i\n"%uint32(operand_a))
        elif instruction["op"] == "file_write":
            self.output_files[instruction["file_name"]].write("%i\n"%int32(operand_a))
        elif instruction["op"] == "read":
            if operand_a not in self.inputs:
                result = 0
            else:
                input_ = self.inputs[operand_a]
                if input_.src_rdy and input_.dst_rdy:
                    result = input_.q
                    input_.next_dst_rdy = False
                else:
                    input_.next_dst_rdy = True
                    wait = True
        elif instruction["op"] == "ready":
            if operand_a not in self.inputs:
                operand_a = 0
            else:
                input_ = self.inputs[operand_a]
                if input_.src_rdy:
                    result = uint32(1)
                else:
                    result = uint32(0)
        elif instruction["op"] == "output_ready":
            if operand_a not in self.outputs:
                operand_a = 0
            else:
                output_ = self.outputs[operand_a]
                if output_.dst_rdy:
                    result = uint32(1)
                else:
                    result = uint32(0)
        elif instruction["op"] == "write":
            if operand_a not in self.outputs:
                pass
            else:
                output_ = self.outputs[operand_a]
                if output_.src_rdy and output_.dst_rdy:
                    output_.next_src_rdy = False
                else:
                    output_.q = operand_b
                    output_.next_src_rdy = True
                    wait = True
        elif instruction["op"] == "float_add":
           a = operand_a
           b = operand_b
           float_ = bits_to_float(a)
           floatb = bits_to_float(b)
           result = float_to_bits(float_ + floatb)
        elif instruction["op"] == "float_subtract":
           a = operand_a
           b = operand_b
           float_ = bits_to_float(a)
           floatb = bits_to_float(b)
           result = float_to_bits(float_ - floatb)
        elif instruction["op"] == "float_multiply":
           a = operand_a
           b = operand_b
           float_ = bits_to_float(a)
           floatb = bits_to_float(b)
           result = float_to_bits(float_ * floatb)
        elif instruction["op"] == "float_divide":
           a = operand_a
           b = operand_b
           float_ = bits_to_float(a)
           floatb = bits_to_float(b)
           try:
               result = float_to_bits(float_ / floatb)
           except ZeroDivisionError:
               result = float_to_bits(float("nan"))
        elif instruction["op"] == "long_float_add":
           double = bits_to_double(join_words(self.a_hi, self.a_lo))
           doubleb = bits_to_double(join_words(self.b_hi, self.b_lo))
           self.a_hi, self.a_lo = split_word(double_to_bits(double + doubleb))
        elif instruction["op"] == "long_float_subtract":
           double = bits_to_double(join_words(self.a_hi, self.a_lo))
           doubleb = bits_to_double(join_words(self.b_hi, self.b_lo))
           self.a_hi, self.a_lo = split_word(double_to_bits(double - doubleb))
        elif instruction["op"] == "long_float_multiply":
           double = bits_to_double(join_words(self.a_hi, self.a_lo))
           doubleb = bits_to_double(join_words(self.b_hi, self.b_lo))
           self.a_hi, self.a_lo = split_word(double_to_bits(double * doubleb))
        elif instruction["op"] == "long_float_divide":
           double = bits_to_double(join_words(self.a_hi, self.a_lo))
           doubleb = bits_to_double(join_words(self.b_hi, self.b_lo))
           try:
               self.a_hi, self.a_lo = split_word(double_to_bits(double / doubleb))
           except ZeroDivisionError:
               self.a_hi, self.a_lo = split_word(double_to_bits(float("nan")))
        elif instruction["op"] == "long_float_file_write":
            long_word = join_words(self.a_hi, self.a_lo)
            self.output_files[instruction["file_name"]].write("%.16f\n"%bits_to_double(long_word))
        elif instruction["op"] == "long_file_write":
            long_word = join_words(self.a_hi, self.a_lo)
            self.output_files[instruction["file_name"]].write("%f\n"%long_word)
        elif instruction["op"] == "assert":
            if operand_a == 0:
                raise ChipsAssertionFail(instruction["file"], instruction["line"])
        elif instruction["op"] == "report":
            print "%d (report (int) at line: %s in file: %s)"%(
                int32(self.a_lo),
                instruction["line"],
                instruction["file"],
            )
        elif instruction["op"] == "long_report":
            print "%d (report (long) at line: %s in file: %s)"%(
                int64(join_words(self.a_hi, self.a_lo)),
                instruction["line"],
                instruction["file"],
            )
        elif instruction["op"] == "float_report":
            print "%f (report (float) at line: %s in file: %s)"%(
                bits_to_float(self.a_lo),
                instruction["line"],
                instruction["file"],
            )
        elif instruction["op"] == "long_float_report":
            print "%s (report (double) at line: %s in file: %s)"%(
                bits_to_double(join_words(self.a_hi, self.a_lo)),
                instruction["line"],
                instruction["file"],
            )
        elif instruction["op"] == "unsigned_report":
            print "%d (report (unsigned) at line: %s in file: %s)"%(
                uint32(self.a_lo),
                instruction["line"],
                instruction["file"],
            )
        elif instruction["op"] == "long_unsigned_report":
            print "%d (report (unsigned long) at line: %s in file: %s)"%(
                uint64(join_words(self.a_hi, self.a_lo)),
                instruction["line"],
                instruction["file"],
            )
        elif instruction["op"] == "wait_clocks":
            if self.timer == operand_a:
                wait = False
                self.timer = 0
            else:
                wait = True
                self.timer += 1

        else:
            print "Unknown machine instruction", instruction["op"]
            sys.exit(-1)

        #Write data back
        if result is not None:
            self.registers[z] = result

        #manipulate stack pointer
        if wait:
            self.program_counter = this_instruction
