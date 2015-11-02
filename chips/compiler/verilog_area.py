#!/usr/bin/env python
"""Generate Verilog Implementation of Instructions

The area optimized implementation uses a CPU like architecture.
+ Instructions are implemented in block RAM.
+ Registers are implemented in dual port RAM.
+ Only one instruction can be executed at a time.
+ The CPU uses a pipeline architecture, and will take 2 clocks to execute a taken branch.
+ A minimal instruction set is determined at compile time, and only those instructions are implemented.

"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2013, Jonathan P Dawson"

from utils import calculate_jumps
from textwrap import dedent


def log2(instructions):
    """Integer only algorithm to calculate the number of bits needed to store a number"""

    bits = 1
    power = 2
    while power < instructions:
        bits += 1
        power *= 2
    return bits


def print_verilog_literal(size, value):
    """Print a verilog literal with expicilt size"""

    if(value >= 0):
        return "%s'd%s" % (size, value)
    else:
        return "-%s'd%s" % (size, abs(value))


def generate_instruction_set(instructions):
    """Calculate the required instruction set"""

    instruction_set = []
    instruction_memory = []
    for instruction in instructions:
        opcode = {}
        encoded_instruction = {}
        encoded_instruction["d"] = 0
        encoded_instruction["c"] = 0
        encoded_instruction["a"] = 0
        encoded_instruction["b"] = 0
        encoded_instruction["literal"] = 0
        if "trace" in instruction:
            encoded_instruction["lineno"] = instruction["trace"].lineno
            encoded_instruction["filename"] = instruction["trace"].filename
        else:
            encoded_instruction["lineno"] = 0
            encoded_instruction["filename"] = "unknown"
        opcode["op"] = instruction["op"]
        opcode["literal"] = False

        if "file_name" in instruction:
            opcode["file_name"] = instruction["file_name"]

        if "file" in instruction:
            opcode["file"] = instruction["file"]

        if "line" in instruction:
            opcode["line"] = instruction["line"]

        if "input" in instruction:
            opcode["input"] = instruction["input"]

        if "output" in instruction:
            opcode["output"] = instruction["output"]

        if "a" in instruction:
            encoded_instruction["a"] = instruction["a"]

        if "b" in instruction:
            encoded_instruction["b"] = instruction["b"]

        if "z" in instruction:
            encoded_instruction["z"] = instruction["z"]

        if "literal" in instruction:
            opcode["literal"] = True
            encoded_instruction["literal"] = instruction["literal"]

        if "label" in instruction:
            opcode["literal"] = True
            encoded_instruction["literal"] = instruction["label"]

        if opcode not in instruction_set:
            instruction_set.append(opcode)

        for op, test_opcode in enumerate(instruction_set):
            if test_opcode == opcode:
                encoded_instruction["op"] = op
                encoded_instruction["comment"] = repr(instruction)
                instruction_memory.append(encoded_instruction)
                break

    return instruction_set, instruction_memory


def generate_declarations(
    instructions,
    no_tb_mode,
    register_bits,
    opcode_bits,
        allocator):
    """Generate verilog declarations"""

    # list all inputs and outputs used in the program
    inputs = allocator.input_names.values()
    outputs = allocator.output_names.values()
    input_files = set([i["file_name"]
                       for i in instructions if "file_read" == i["op"]])
    output_files = set([i["file_name"]
                        for i in instructions if i["op"] in ("file_write", "float_file_write", "long_float_file_write")])
    testbench = not inputs and not outputs and not no_tb_mode

    # Do not generate a port in testbench mode
    inports = [
        ("input_" + i, 32) for i in inputs
    ] + [
        ("input_" + i + "_stb", 1) for i in inputs
    ] + [
        ("output_" + i + "_ack", 1) for i in outputs
    ]

    outports = [
        ("output_" + i, 32) for i in outputs
    ] + [
        ("output_" + i + "_stb", 1) for i in outputs
    ] + [
        ("input_" + i + "_ack", 1) for i in inputs
    ]

    # create list of signals
    signals = [
        ("timer", 32),
        ("timer_clock", 64),
        ("program_counter", 16),
        ("program_counter_1", 16),
        ("program_counter_2", 16),
        ("instruction", 32 + 8 + opcode_bits),
        ("opcode_2", opcode_bits),

        ("a", 4),
        ("b", 4),
        ("z", 4),

        ("write_enable", 1),
        ("address_a_2", 4),
        ("address_b_2", 4),
        ("address_z_2", 4),
        ("address_z_3", 4),

        ("load_data", 32),
        ("write_output", 32),
        ("write_value", 32),
        ("read_input", 32),

        ("literal_2", 16),
        ("a_hi", 32),
        ("b_hi", 32),
        ("a_lo", 32),
        ("b_lo", 32),
        ("long_result", 64),
        ("result", 32),
        ("address", 16),
        ("data_out", 32),
        ("data_in", 32),
        ("carry", 32),
    ] + [
        ("s_output_" + i + "_stb", 32) for i in outputs
    ] + [
        ("s_output_" + i, 32) for i in outputs
    ] + [
        ("s_input_" + i + "_ack", 32) for i in inputs
    ]

    if testbench:
        signals.append(("clk", 1))
        signals.append(("rst", 1))
    else:
        inports.append(("clk", 1))
        inports.append(("rst", 1))

    return inputs, outputs, input_files, output_files, testbench, inports, outports, signals


def floating_point_enables(instruction_set):
    floating_point_arithmetic = []
    floating_point_conversions = []
    floating_point_debug = []
    for i in instruction_set:
        if i["op"] == "float_add":
            floating_point_arithmetic.append("adder")
        if i["op"] == "float_subtract":
            floating_point_arithmetic.append("adder")
        if i["op"] == "float_multiply":
            floating_point_arithmetic.append("multiplier")
        if i["op"] == "float_divide":
            floating_point_arithmetic.append("divider")
        if i["op"] == "long_float_add":
            floating_point_arithmetic.append("double_adder")
        if i["op"] == "long_float_subtract":
            floating_point_arithmetic.append("double_adder")
        if i["op"] == "long_float_multiply":
            floating_point_arithmetic.append("double_multiplier")
        if i["op"] == "long_float_divide":
            floating_point_arithmetic.append("double_divider")
        if i["op"] == "int_to_float":
            floating_point_conversions.append("int_to_float")
        if i["op"] == "float_to_int":
            floating_point_conversions.append("float_to_int")
        if i["op"] == "long_to_double":
            floating_point_conversions.append("long_to_double")
        if i["op"] == "double_to_long":
            floating_point_conversions.append("double_to_long")
        if i["op"] == "float_to_double":
            floating_point_conversions.append("float_to_double")
        if i["op"] == "double_to_float":
            floating_point_conversions.append("double_to_float")
        if i["op"] == "float_report":
            floating_point_debug.append("float_report")
        if i["op"] == "long_float_report":
            floating_point_debug.append("long_float_report")
        if i["op"] == "float_file_write":
            floating_point_debug.append("float_report")
        if i["op"] == "long_float_file_write":
            floating_point_debug.append("long_float_report")

    floating_point_arithmetic = set(floating_point_arithmetic)
    floating_point_conversions = set(floating_point_conversions)
    floating_point_debug = set(floating_point_debug)

    return floating_point_arithmetic, floating_point_conversions, floating_point_debug


def generate_CHIP(input_file,
                  name,
                  instructions,
                  output_file,
                  allocator,
                  initialize_memory,
                  memory_size=1024,
                  no_tb_mode=False):
    """A big ugly function to crunch through all the instructions and generate the CHIP equivilent"""

    instructions = calculate_jumps(instructions)
    instruction_set, instruction_memory = generate_instruction_set(
        instructions)
    register_bits = 16
    opcode_bits = log2(len(instruction_set))
    instruction_bits = 16 + 4 + 4 + opcode_bits
    declarations = generate_declarations(
        instructions,
        no_tb_mode,
        register_bits,
        opcode_bits,
        allocator)
    inputs, outputs, input_files, output_files, testbench, inports, outports, signals = declarations
    floating_point_arithmetic, floating_point_conversions, floating_point_debug = floating_point_enables(
        instruction_set)

    # output the code in verilog
    output_file.write("//name : %s\n" % name)
    for i in inputs:
        output_file.write("//input : input_%s:16\n" % i)
    for i in outputs:
        output_file.write("//output : output_%s:16\n" % i)
    output_file.write("//source_file : %s\n" % input_file)
    output_file.write(dedent("""
    ///+============================================================================+
    ///|                                                                            |
    ///|                     This file was generated by Chips                       |
    ///|                                                                            |
    ///|                                  Chips                                     |
    ///|                                                                            |
    ///|                      http://github.com/dawsonjon/Chips-2.0                 |
    ///|                                                                            |
    ///|                                                             Python powered |
    ///+============================================================================+
    """))

    output_file.write("module %s" % name)

    all_ports = [name for name, size in inports + outports] + ["exception"]
    if all_ports:
        output_file.write("(")
        output_file.write(",".join(all_ports))
        output_file.write(");\n")
    else:
        output_file.write(";\n")

    output_file.write("  integer file_count;\n")

    for i in floating_point_arithmetic:

        if i.startswith("double"):
            output_file.write("  reg [63:0] %s_a;\n" % (i))
            output_file.write("  reg [63:0] %s_b;\n" % (i))
            output_file.write("  wire [63:0] %s_z;\n" % (i))
        else:
            output_file.write("  reg [31:0] %s_a;\n" % (i))
            output_file.write("  reg [31:0] %s_b;\n" % (i))
            output_file.write("  wire [31:0] %s_z;\n" % (i))

        output_file.write("  reg %s_a_stb;\n" % (i))
        output_file.write("  wire %s_a_ack;\n" % (i))
        output_file.write("  reg %s_b_stb;\n" % (i))
        output_file.write("  wire %s_b_ack;\n" % (i))
        output_file.write("  wire %s_z_stb;\n" % (i))
        output_file.write("  reg %s_z_ack;\n" % (i))

    for i in floating_point_conversions:

        if i.startswith("long") or i.startswith("double"):
            output_file.write("  reg [63:0] %s_in;\n" % (i))
        else:
            output_file.write("  reg [31:0] %s_in;\n" % (i))

        if i.endswith("long") or i.endswith("double"):
            output_file.write("  wire [63:0] %s_out;\n" % (i))
        else:
            output_file.write("  wire [31:0] %s_out;\n" % (i))

        output_file.write("  wire %s_out_stb;\n" % (i))
        output_file.write("  reg %s_out_ack;\n" % (i))
        output_file.write("  reg %s_in_stb;\n" % (i))
        output_file.write("  wire %s_in_ack;\n" % (i))

    if floating_point_debug:
        output_file.write("  real fp_value;\n")

    states = [
        "stop",
        "instruction_fetch",
        "operand_fetch",
        "execute",
        "load",
        "wait_state",
    ]

    if inports:
        states.append("read")

    if outports:
        states.append("write")

    for i in floating_point_arithmetic:
        states.append("%s_write_a" % i)
        states.append("%s_write_b" % i)
        states.append("%s_read_z" % i)

    for i in floating_point_conversions:
        states.append("%s_write_a" % i)
        states.append("%s_read_z" % i)

    state_variables = []
    for index, state in enumerate(states):
        state_variables.append(
            "%s = %s'd%s" %
            (state, log2(len(states)), index))

    signals.append(("state", len(state_variables)))
    output_file.write("  parameter  ")
    output_file.write(",\n  ".join(state_variables))
    output_file.write(";\n")

    input_files = dict(
        zip(input_files, ["input_file_%s" %
                          i for i, j in enumerate(input_files)]))
    for i in input_files.values():
        output_file.write("  integer %s;\n" % i)

    output_files = dict(
        zip(output_files, ["output_file_%s" %
                           i for i, j in enumerate(output_files)]))
    for i in output_files.values():
        output_file.write("  integer %s;\n" % i)

    def write_declaration(object_type, name, size):
        if size == 1:
            output_file.write(object_type)
            output_file.write(name)
            output_file.write(";\n")
        else:
            output_file.write(object_type)
            output_file.write("[%i:0]" % (size - 1))
            output_file.write(" ")
            output_file.write(name)
            output_file.write(";\n")

    for name, size in inports:
        write_declaration("  input ", name, size)

    for name, size in outports:
        write_declaration("  output ", name, size)

    for name, size in signals:
        write_declaration("  reg ", name, size)

    output_file.write("  output reg exception;\n")
    output_file.write(
        "  reg [%s:0] instructions [%i:0];\n" %
        (instruction_bits - 1, len(instructions) - 1))
    output_file.write("  reg [31:0] memory [%i:0];\n" % memory_size)
    output_file.write("  reg [31:0] registers [15:0];\n")
    output_file.write("  wire [31:0] operand_a;\n")
    output_file.write("  wire [31:0] operand_b;\n")
    output_file.write("  wire [31:0] register_a;\n")
    output_file.write("  wire [31:0] register_b;\n")
    output_file.write("  wire [15:0] literal;\n")
    output_file.write("  wire [%s:0] opcode;\n" % (opcode_bits - 1))
    output_file.write("  wire [3:0] address_a;\n")
    output_file.write("  wire [3:0] address_b;\n")
    output_file.write("  wire [3:0] address_z;\n")
    output_file.write("  wire [15:0] load_address;\n")
    output_file.write("  wire [15:0] store_address;\n")
    output_file.write("  wire [31:0] store_data;\n")
    output_file.write("  wire  store_enable;\n")

    # generate clock and reset in testbench mode
    if testbench:

        output_file.write(
            "\n  //////////////////////////////////////////////////////////////////////////////\n")
        output_file.write(
            "  // CLOCK AND RESET GENERATION                                                 \n")
        output_file.write(
            "  //                                                                            \n")
        output_file.write(
            "  // This file was generated in test bench mode. In this mode, the verilog      \n")
        output_file.write(
            "  // output file can be executed directly within a verilog simulator.           \n")
        output_file.write(
            "  // In test bench mode, a simulated clock and reset signal are generated within\n")
        output_file.write(
            "  // the output file.                                                           \n")
        output_file.write(
            "  // Verilog files generated in testbecnch mode are not suitable for synthesis, \n")
        output_file.write(
            "  // or for instantiation within a larger design.\n")

        output_file.write("  \n  initial\n")
        output_file.write("  begin\n")
        output_file.write("    rst <= 1'b1;\n")
        output_file.write("    #50 rst <= 1'b0;\n")
        output_file.write("  end\n\n")

        output_file.write("  \n  initial\n")
        output_file.write("  begin\n")
        output_file.write("    clk <= 1'b0;\n")
        output_file.write("    while (1) begin\n")
        output_file.write("      #5 clk <= ~clk;\n")
        output_file.write("    end\n")
        output_file.write("  end\n\n")

    # Instance Floating Point Arithmetic
    if floating_point_arithmetic or floating_point_conversions:

        output_file.write(
            "\n  //////////////////////////////////////////////////////////////////////////////\n")
        output_file.write(
            "  // Floating Point Arithmetic                                                  \n")
        output_file.write(
            "  //                                                                            \n")
        output_file.write(
            "  // Generate IEEE 754 single precision divider, adder and multiplier           \n")
        output_file.write(
            "  //                                                                            \n")

        for i in floating_point_arithmetic:
            output_file.write("  %s %s_inst(\n" % (i, i))
            output_file.write("    .clk(clk),\n")
            output_file.write("    .rst(rst),\n")
            output_file.write("    .input_a(%s_a),\n" % i)
            output_file.write("    .input_a_stb(%s_a_stb),\n" % i)
            output_file.write("    .input_a_ack(%s_a_ack),\n" % i)
            output_file.write("    .input_b(%s_b),\n" % i)
            output_file.write("    .input_b_stb(%s_b_stb),\n" % i)
            output_file.write("    .input_b_ack(%s_b_ack),\n" % i)
            output_file.write("    .output_z(%s_z),\n" % i)
            output_file.write("    .output_z_stb(%s_z_stb),\n" % i)
            output_file.write("    .output_z_ack(%s_z_ack)\n" % i)
            output_file.write("  );\n")

        for i in floating_point_conversions:
            output_file.write("  %s %s_inst(\n" % (i, i))
            output_file.write("    .clk(clk),\n")
            output_file.write("    .rst(rst),\n")
            output_file.write("    .input_a(%s_in),\n" % i)
            output_file.write("    .input_a_stb(%s_in_stb),\n" % i)
            output_file.write("    .input_a_ack(%s_in_ack),\n" % i)
            output_file.write("    .output_z(%s_out),\n" % i)
            output_file.write("    .output_z_stb(%s_out_stb),\n" % i)
            output_file.write("    .output_z_ack(%s_out_ack)\n" % i)
            output_file.write("  );\n")

    # Generate a state machine to execute the instructions
    # if initialize_memory and allocator.memory_content:
#
        # output_file.write("\n  //////////////////////////////////////////////////////////////////////////////\n")
        # output_file.write("  // MEMORY INITIALIZATION                                                      \n")
        # output_file.write("  //                                                                            \n")
        # output_file.write("  // In order to reduce program size, array contents have been stored into      \n")
        # output_file.write("  // memory at initialization. In an FPGA, this will result in the memory being \n")
        # output_file.write("  // initialized when the FPGA configures.                                      \n")
        # output_file.write("  // Memory will not be re-initialized at reset.                                \n")
        # output_file.write("  // Dissable this behaviour using the no_initialize_memory switch              \n")
#
        # output_file.write("  \n  initial\n")
        # output_file.write("  begin\n")
        # for location, content in allocator.memory_content.iteritems():
            # output_file.write("    memory[%s] = %s;\n"%(location, content))
        # output_file.write("  end\n\n")
    output_file.write(
        "\n  //////////////////////////////////////////////////////////////////////////////\n")
    output_file.write(
        "  // INSTRUCTION INITIALIZATION                                                 \n")
    output_file.write(
        "  //                                                                            \n")
    output_file.write(
        "  // Initialise the contents of the instruction memory                          \n")
    output_file.write("  //\n")
    output_file.write("  // Intruction Set\n")
    output_file.write("  // ==============\n")
    for num, opcode in enumerate(instruction_set):
        output_file.write("  // %s %s\n" % (num, opcode))

    output_file.write("  // Intructions\n")
    output_file.write("  // ===========\n")
    output_file.write("  \n  initial\n")
    output_file.write("  begin\n")
    for location, instruction in enumerate(instruction_memory):
        # print instruction
        output_file.write("    instructions[%s] = {%s, %s, %s, %s};//%s : %s %s\n" % (
            location,
            print_verilog_literal(opcode_bits, instruction["op"]),
            print_verilog_literal(4, instruction.get("z", 0)),
            print_verilog_literal(4, instruction.get("a", 0)),
            print_verilog_literal(
            16, instruction["literal"] | instruction.get("b", 0)),
            instruction["filename"],
            instruction["lineno"],
            instruction["comment"],
        ))
    output_file.write("  end\n\n")

    if input_files or output_files:

        output_file.write(
            "\n  //////////////////////////////////////////////////////////////////////////////\n")
        output_file.write(
            "  // OPEN FILES                                                                 \n")
        output_file.write(
            "  //                                                                            \n")
        output_file.write(
            "  // Open all files used at the start of the process                            \n")

        output_file.write("  \n  initial\n")
        output_file.write("  begin\n")
        for file_name, file_ in input_files.iteritems():
            output_file.write(
                "    %s = $fopenr(\"%s\");\n" %
                (file_, file_name))
        for file_name, file_ in output_files.iteritems():
            output_file.write(
                "    %s = $fopen(\"%s\");\n" %
                (file_, file_name))
        output_file.write("  end\n\n")

    output_file.write("  \n  always @(posedge clk)\n")
    output_file.write("  begin\n")
    output_file.write("    load_data <= memory[load_address];\n")
    output_file.write("    if(store_enable && state == execute) begin\n")
    output_file.write("      memory[store_address] <= store_data;\n")
    output_file.write("    end\n")
    output_file.write("  end\n\n")

    output_file.write(
        "\n  //////////////////////////////////////////////////////////////////////////////\n")
    output_file.write("  // PIPELINE STAGE 1 -- FETCH INSTRUCTION\n")
    output_file.write(
        "  //                                                                            \n")
    output_file.write("  \n  always @(posedge clk)\n")
    output_file.write("  begin\n")
    output_file.write("    //implement memory for instructions\n")
    output_file.write(
        "    if (state == instruction_fetch || state == operand_fetch || state == execute) begin\n")
    output_file.write("      instruction <= instructions[program_counter];\n")
    output_file.write("      program_counter_1 <= program_counter;\n")
    output_file.write("    end\n")
    output_file.write("  end\n\n")
    output_file.write("  assign opcode    = instruction[%s:%s];\n" % (
        instruction_bits - 1,
        instruction_bits - opcode_bits))
    output_file.write("  assign address_z = instruction[23:20];\n")
    output_file.write("  assign address_a = instruction[19:16];\n")
    output_file.write("  assign address_b = instruction[3:0];\n")
    output_file.write("  assign literal   = instruction[15:0];\n")

    output_file.write(
        "\n  //////////////////////////////////////////////////////////////////////////////\n")
    output_file.write("  // PIPELINE STAGE 2 -- FETCH OPERANDS\n")
    output_file.write(
        "  //                                                                            \n")
    output_file.write("  \n  always @(posedge clk)\n")
    output_file.write("  begin\n")
    output_file.write("    if (write_enable) begin\n")
    output_file.write("      registers[address_z_3] <= result;\n")
    output_file.write("    end\n")
    output_file.write(
        "    if (state == operand_fetch || state == execute) begin\n")
    output_file.write("      opcode_2 <= opcode;\n")
    output_file.write("      literal_2 <= literal;\n")
    output_file.write("      address_a_2 <= address_a;\n")
    output_file.write("      address_b_2 <= address_b;\n")
    output_file.write("      address_z_2 <= address_z;\n")
    output_file.write("      program_counter_2 <= program_counter_1;\n")
    output_file.write("    end\n")
    output_file.write("  end\n")
    output_file.write("  assign register_a = registers[address_a_2];\n")
    output_file.write("  assign register_b = registers[address_b_2];\n")
    output_file.write(
        "  assign operand_a = (address_a_2 == address_z_3 && write_enable)?result:register_a;\n")
    output_file.write(
        "  assign operand_b = (address_b_2 == address_z_3 && write_enable)?result:register_b;\n")
    output_file.write("  assign store_address = operand_a;\n")
    output_file.write("  assign load_address = operand_a;\n")
    output_file.write("  assign store_data = operand_b;\n")

    store_opcode = 0
    for opcode, instruction in enumerate(instruction_set):
        if instruction["op"] == "store":
            store_opcode = opcode

    output_file.write(
        "  assign store_enable = (opcode_2==%s);\n" %
        store_opcode)

    output_file.write(
        "\n  //////////////////////////////////////////////////////////////////////////////\n")
    output_file.write("  // PIPELINE STAGE 3 -- EXECUTE\n")
    output_file.write(
        "  //                                                                            \n")

    output_file.write("  \n  always @(posedge clk)\n")
    output_file.write("  begin\n\n")
    output_file.write("  write_enable <= 0;\n")
    output_file.write("  case(state)\n\n")
    output_file.write("    //instruction_fetch\n")
    output_file.write("    instruction_fetch: begin\n")
    output_file.write("      program_counter <= program_counter + 1;\n")
    output_file.write("      state <= operand_fetch;\n")
    output_file.write("    end\n")
    output_file.write("    //operand_fetch\n")
    output_file.write("    operand_fetch: begin\n")
    output_file.write("      program_counter <= program_counter + 1;\n")
    output_file.write("      state <= execute;\n")
    output_file.write("    end\n")
    output_file.write("    //execute\n")
    output_file.write("    execute: begin\n")
    # output_file.write("      $display(program_counter_2);\n")
    output_file.write("      program_counter <= program_counter + 1;\n")
    output_file.write("      address_z_3 <= address_z_2;\n")
    output_file.write("      case(opcode_2)\n\n")

    # A frame is executed in each state
    for opcode, instruction in enumerate(instruction_set):

        output_file.write("        //%s\n" % (instruction["op"]))
        output_file.write("        16'd%s:\n" % (opcode))
        output_file.write("        begin\n")

        if instruction["op"] == "nop":
            pass

        elif instruction["op"] == "literal":
            output_file.write("          result<=$signed(literal_2);\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "addl":
            output_file.write("          result<=operand_a + literal_2;\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "literal_hi":
            output_file.write(
                "          result<= {literal_2, operand_a[15:0]};\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "store":
            pass

        elif instruction["op"] == "load":
            output_file.write("          state <= load;\n")

        elif instruction["op"] == "call":
            output_file.write("          result <= program_counter_2 + 1;\n")
            output_file.write("          write_enable <= 1;\n")
            output_file.write("          program_counter <= literal_2;\n")
            output_file.write("          state <= instruction_fetch;\n")

        elif instruction["op"] == "return":
            output_file.write("          program_counter <= operand_a;\n")
            output_file.write("          state <= instruction_fetch;\n")

        elif instruction["op"] == "a_lo":
            output_file.write("          a_lo <= operand_a;\n")
            output_file.write("          result <= a_lo;\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "b_lo":
            output_file.write("          b_lo <= operand_a;\n")
            output_file.write("          result <= b_lo;\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "a_hi":
            output_file.write("          a_hi <= operand_a;\n")
            output_file.write("          result <= a_hi;\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "b_hi":
            output_file.write("          b_hi <= operand_a;\n")
            output_file.write("          result <= b_hi;\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "not":
            output_file.write("          result <= ~operand_a;\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "int_to_long":
            output_file.write("          if(operand_a[31]) begin\n")
            output_file.write("            result <= -1;\n")
            output_file.write("          end else begin\n")
            output_file.write("            result <= 0;\n")
            output_file.write("          end\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "int_to_float":
            output_file.write("          int_to_float_in <= a_lo;\n")
            output_file.write("          state <= int_to_float_write_a;\n")

        elif instruction["op"] == "float_to_int":
            output_file.write("          float_to_int_in <= a_lo;\n")
            output_file.write("          state <= float_to_int_write_a;\n")

        elif instruction["op"] == "long_to_double":
            output_file.write("          long_to_double_in <= {a_hi, a_lo};\n")
            output_file.write("          state <= long_to_double_write_a;\n")

        elif instruction["op"] == "double_to_long":
            output_file.write("          double_to_long_in <= {a_hi, a_lo};\n")
            output_file.write("          state <= double_to_long_write_a;\n")

        elif instruction["op"] == "float_to_double":
            output_file.write("          float_to_double_in <= a_lo;\n")
            output_file.write("          state <= float_to_double_write_a;\n")

        elif instruction["op"] == "double_to_float":
            output_file.write(
                "          double_to_float_in <= {a_hi, a_lo};\n")
            output_file.write("          state <= double_to_float_write_a;\n")

        elif instruction["op"] == "add":
            output_file.write(
                "          long_result = operand_a + operand_b;\n")
            output_file.write("          result <= long_result[31:0];\n")
            output_file.write("          carry[0] <= long_result[32];\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "add_with_carry":
            output_file.write(
                "          long_result = operand_a + operand_b + carry[0];\n")
            output_file.write("          result <= long_result[31:0];\n")
            output_file.write("          carry[0] <= long_result[32];\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "subtract":
            output_file.write(
                "          long_result = operand_a + (~operand_b) + 1;\n")
            output_file.write("          result <= long_result[31:0];\n")
            output_file.write("          carry[0] <= ~long_result[32];\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "subtract_with_carry":
            output_file.write(
                "          long_result = operand_a + (~operand_b) + carry[0];\n")
            output_file.write("          result <= long_result[31:0];\n")
            output_file.write("          carry[0] <= ~long_result[32];\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "multiply":
            output_file.write(
                "          long_result = operand_a * operand_b;\n")
            output_file.write("          result <= long_result[31:0];\n")
            output_file.write("          carry <= long_result[63:32];\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "carry":
            output_file.write("          result <= carry;\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "or":
            output_file.write("          result <= operand_a | operand_b;\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "and":
            output_file.write("          result <= operand_a & operand_b;\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "xor":
            output_file.write("          result <= operand_a ^ operand_b;\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "shift_left":
            output_file.write("          if(operand_b < 32) begin\n")
            output_file.write(
                "            result <= operand_a << operand_b;\n")
            output_file.write(
                "            carry <= operand_a >> (32-operand_b);\n")
            output_file.write("          end else begin\n")
            output_file.write("            result <= 0;\n")
            output_file.write("            carry <= operand_a;\n")
            output_file.write("          end\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "shift_left_with_carry":
            output_file.write("          if(operand_b < 32) begin\n")
            output_file.write(
                "            result <= (operand_a << operand_b) | carry;\n")
            output_file.write("          end else begin\n")
            output_file.write("            result <= carry;\n")
            output_file.write("          end\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "shift_right":
            output_file.write("          if(operand_b < 32) begin\n")
            output_file.write(
                "            result <= $signed(operand_a) >>> operand_b;\n")
            output_file.write(
                "            carry <= operand_a << (32-operand_b);\n")
            output_file.write("          end else begin\n")
            output_file.write("            result <= operand_a[31]?-1:0;\n")
            output_file.write("            carry <= operand_a;\n")
            output_file.write("          end\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "unsigned_shift_right":
            output_file.write("          if(operand_b < 32) begin\n")
            output_file.write(
                "            result <= operand_a >> operand_b;\n")
            output_file.write(
                "            carry <= operand_a << (32-operand_b);\n")
            output_file.write("          end else begin\n")
            output_file.write("            result <= 0;\n")
            output_file.write("            carry <= operand_a;\n")
            output_file.write("          end\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "shift_right_with_carry":
            output_file.write("          if(operand_b < 32) begin\n")
            output_file.write(
                "            result <= (operand_a >> operand_b) | carry;\n")
            output_file.write("          end else begin\n")
            output_file.write("            result <= carry;\n")
            output_file.write("          end\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "greater":
            output_file.write(
                "          result <= $signed(operand_a) > $signed(operand_b);\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "greater_equal":
            output_file.write(
                "          result <= $signed(operand_a) >= $signed(operand_b);\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "unsigned_greater":
            output_file.write(
                "          result <= $unsigned(operand_a) > $unsigned(operand_b);\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "unsigned_greater_equal":
            output_file.write(
                "          result <= $unsigned(operand_a) >= $unsigned(operand_b);\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "equal":
            output_file.write("          result <= operand_a == operand_b;\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "not_equal":
            output_file.write("          result <= operand_a != operand_b;\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "float_add":
            output_file.write("          adder_a_stb <= 1;\n")
            output_file.write("          adder_a <= operand_a;\n")
            output_file.write("          adder_b <= operand_b;\n")
            output_file.write("          state <= adder_write_a;\n")

        elif instruction["op"] == "float_subtract":
            output_file.write("          adder_a_stb <= 1;\n")
            output_file.write("          adder_a <= operand_a;\n")
            output_file.write(
                "          adder_b <= {~operand_b[31], operand_b[30:0]};\n")
            output_file.write("          state <= adder_write_a;\n")

        elif instruction["op"] == "float_multiply":
            output_file.write("          multiplier_a_stb <= 1;\n")
            output_file.write("          multiplier_a <= operand_a;\n")
            output_file.write("          multiplier_b <= operand_b;\n")
            output_file.write("          state <= multiplier_write_a;\n")

        elif instruction["op"] == "float_divide":
            output_file.write("          divider_a_stb <= 1;\n")
            output_file.write("          divider_a <= operand_a;\n")
            output_file.write("          divider_b <= operand_b;\n")
            output_file.write("          state <= divider_write_a;\n")

        elif instruction["op"] == "long_float_add":
            output_file.write("          double_adder_a <= {a_hi, a_lo};\n")
            output_file.write("          double_adder_b <= {b_hi, b_lo};\n")
            output_file.write("          state <= double_adder_write_a;\n")

        elif instruction["op"] == "long_float_subtract":
            output_file.write("          double_adder_a <= {a_hi, a_lo};\n")
            output_file.write(
                "          double_adder_b <= {~b_hi[31], b_hi[30:0], b_lo};\n")
            output_file.write("          state <= double_adder_write_a;\n")

        elif instruction["op"] == "long_float_multiply":
            output_file.write(
                "          double_multiplier_a <= {a_hi, a_lo};\n")
            output_file.write(
                "          double_multiplier_b <= {b_hi, b_lo};\n")
            output_file.write(
                "          state <= double_multiplier_write_a;\n")

        elif instruction["op"] == "long_float_divide":
            output_file.write("          double_divider_a <= {a_hi, a_lo};\n")
            output_file.write("          double_divider_b <= {b_hi, b_lo};\n")
            output_file.write("          state <= double_divider_write_a;\n")

        elif instruction["op"] == "jmp_if_false":
            output_file.write("          if (operand_a == 0) begin\n")
            output_file.write("            program_counter <= literal_2;\n")
            output_file.write("            state <= instruction_fetch;\n")
            output_file.write("          end\n")

        elif instruction["op"] == "jmp_if_true":
            output_file.write("          if (operand_a != 0) begin\n")
            output_file.write("            program_counter <= literal_2;\n")
            output_file.write("            state <= instruction_fetch;\n")
            output_file.write("          end\n")

        elif instruction["op"] == "goto":
            output_file.write("          program_counter <= literal_2;\n")
            output_file.write("          state <= instruction_fetch;\n")

        elif instruction["op"] == "file_read":
            output_file.write("        16'd%s:\n" % (opcode))
            output_file.write("        begin\n")
            output_file.write("          file_count = $fscanf(%s, \"%%d\\n\", result);\n" % (
                              input_files[instruction["file_name"]]))
            output_file.write("          write_enable <= 1;\n")
            output_file.write("        end\n\n")

        elif instruction["op"] == "float_file_write":
            output_file.write('          long_result[63] = operand_a[31];\n')
            output_file.write('          if (operand_a[30:23] == 0) begin\n')
            output_file.write('              long_result[62:52] = 0;\n')
            output_file.write(
                '          end else if (operand_a[30:23] == 127) begin\n')
            output_file.write('              long_result[62:52] = 1023;\n')
            output_file.write('          end else begin\n')
            output_file.write(
                '              long_result[62:52] = (operand_a[30:23] - 127) + 1023;\n')
            output_file.write('          end\n')
            output_file.write(
                '          long_result[51:29] = operand_a[22:0];\n')
            output_file.write('          long_result[28:0] = 0;\n')
            output_file.write(
                '          fp_value = $bitstoreal(long_result);\n')
            output_file.write('          $fdisplay (%s, "%%g", fp_value);\n' % (
                              output_files[
                              instruction["file_name"]]))

        elif instruction["op"] == "long_float_file_write":
            output_file.write(
                '          fp_value = $bitstoreal({a_hi, a_lo});\n')
            output_file.write('          $fdisplay (%s, "%%g", fp_value);\n' % (
                              output_files[
                              instruction["file_name"]]))

        elif instruction["op"] == "unsigned_file_write":
            output_file.write("          $fdisplay (%s, \"%%d\", $unsigned(operand_a));\n" % (
                              output_files[instruction["file_name"]]))

        elif instruction["op"] == "file_write":
            output_file.write("          $fdisplay (%s, \"%%d\", $signed(operand_a));\n" % (
                              output_files[instruction["file_name"]]))

        elif instruction["op"] == "read":
            output_file.write("          state <= read;\n")
            output_file.write("          read_input <= operand_a;\n")

        elif instruction["op"] == "ready":
            output_file.write("          result <= 0;\n")
            output_file.write("          case(operand_a)\n\n")
            for handle, input_name in allocator.input_names.iteritems():
                output_file.write("            %s:\n" % (handle))
                output_file.write("            begin\n")
                output_file.write(
                    "              result[0] <= input_%s_stb;\n" %
                    input_name)
                output_file.write("            end\n")
            output_file.write("          endcase\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "output_ready":
            output_file.write("          result <= 0;\n")
            output_file.write("          case(operand_a)\n\n")
            for handle, output_name in allocator.output_names.iteritems():
                output_file.write("            %s:\n" % (handle))
                output_file.write("            begin\n")
                output_file.write(
                    "              result[0] <= output_%s_ack;\n" %
                    output_name)
                output_file.write("            end\n")
            output_file.write("          endcase\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "write":
            output_file.write("          state <= write;\n")
            output_file.write("          write_output <= operand_a;\n")
            output_file.write("          write_value <= operand_b;\n")

        elif instruction["op"] == "assert":
            output_file.write("          if (operand_a == 0) begin\n")
            output_file.write("            $display(\"Assertion failed at line: %s in file: %s\");\n" % (
                              instruction["line"],
                              instruction["file"]))
            output_file.write("            $finish_and_return(1);\n")
            output_file.write("          end\n")

        elif instruction["op"] == "wait_clocks":
            output_file.write("          timer <= operand_a;\n")
            output_file.write("          state <= wait_state;\n")

        elif instruction["op"] == "timer_low":
            output_file.write("          result <= timer_clock[31:0];\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "timer_high":
            output_file.write("          result <= timer_clock[63:32];\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "report":
            output_file.write('          $display ("%%d (report (int) at line: %s in file: %s)", $signed(a_lo));\n' % (
                instruction["line"],
                instruction["file"],))

        elif instruction["op"] == "long_report":
            output_file.write('          $display ("%%d (report (long) at line: %s in file: %s)", $signed({a_hi, a_lo}));\n' % (
                instruction["line"],
                instruction["file"],))

        elif instruction["op"] == "float_report":
            output_file.write('          long_result[63] = a_lo[31];\n')
            output_file.write('          if (a_lo[30:23] == 0) begin\n')
            output_file.write('              long_result[62:52] = 0;\n')
            output_file.write(
                '          end else if (a_lo[30:23] == 255) begin\n')
            output_file.write('              long_result[62:52] = 2047;\n')
            output_file.write('          end else begin\n')
            output_file.write(
                '              long_result[62:52] = (a_lo[30:23] - 127) + 1023;\n')
            output_file.write('          end\n')
            output_file.write('          long_result[51:29] = a_lo[22:0];\n')
            output_file.write('          long_result[28:0] = 0;\n')
            output_file.write(
                '          fp_value = $bitstoreal(long_result);\n')
            output_file.write('          $display ("%%f (report (float) at line: %s in file: %s)", fp_value);\n' % (
                              instruction["line"],
                              instruction["file"]))

        elif instruction["op"] == "long_float_report":
            output_file.write(
                '          fp_value = $bitstoreal({a_hi, a_lo});\n')
            output_file.write('          $display ("%%f (report (double) at line: %s in file: %s)", fp_value);\n' % (
                              instruction["line"],
                              instruction["file"]))

        elif instruction["op"] == "unsigned_report":
            output_file.write('          $display ("%%d (report (unsigned) at line: %s in file: %s)", $unsigned(a_lo));\n' % (
                instruction["line"],
                instruction["file"]))

        elif instruction["op"] == "long_unsigned_report":
            output_file.write('          $display ("%%d (report (unsigned long) at line: %s in file: %s)", $unsigned({a_hi, a_lo}));\n' % (
                instruction["line"],
                instruction["file"]))

        elif instruction["op"] == "stop":
            # If we are in testbench mode stop the simulation
            # If we are part of a larger design, other C programs may still be
            # running
            for file_ in input_files.values():
                output_file.write("          $fclose(%s);\n" % file_)
            for file_ in output_files.values():
                output_file.write("          $fclose(%s);\n" % file_)
            if testbench:
                output_file.write('          $finish;\n')
            output_file.write('        state <= stop;\n')

        else:
            print "unsuported instruction", instruction["op"]
            print instruction

        output_file.write("        end\n\n")
    output_file.write("      endcase\n\n")
    output_file.write("    end\n\n")

    if allocator.input_names:
        output_file.write("    read:\n")
        output_file.write("    begin\n")
        output_file.write("      case(read_input)\n")
        for handle, input_name in allocator.input_names.iteritems():
            output_file.write("      %s:\n" % (handle))
            output_file.write("      begin\n")
            output_file.write("        s_input_%s_ack <= 1;\n" % input_name)
            output_file.write("        if (s_input_%s_ack && input_%s_stb) begin\n" % (
                              input_name,
                              input_name))
            output_file.write("          result <= input_%s;\n" % input_name)
            output_file.write("          write_enable <= 1;\n")
            output_file.write("          s_input_%s_ack <= 0;\n" % input_name)
            output_file.write("          state <= execute;\n")
            output_file.write("        end\n")
            output_file.write("      end\n")
        output_file.write("      endcase\n")
        output_file.write("    end\n\n")

    if allocator.output_names:
        output_file.write("    write:\n")
        output_file.write("    begin\n")
        output_file.write("      case(write_output)\n")
        for handle, output_name in allocator.output_names.iteritems():
            output_file.write("      %s:\n" % (handle))
            output_file.write("      begin\n")
            output_file.write("        s_output_%s_stb <= 1;\n" % output_name)
            output_file.write(
                "        s_output_%s <= write_value;\n" %
                output_name)
            output_file.write("        if (output_%s_ack && s_output_%s_stb) begin\n" % (
                              output_name,
                              output_name))
            output_file.write(
                "          s_output_%s_stb <= 0;\n" %
                output_name)
            output_file.write("          state <= execute;\n")
            output_file.write("        end\n")
            output_file.write("      end\n")
        output_file.write("      endcase\n")
        output_file.write("    end\n\n")

    output_file.write("    load:\n")
    output_file.write("    begin\n")
    output_file.write("        result <= load_data;\n")
    output_file.write("        write_enable <= 1;\n")
    output_file.write("        state <= execute;\n")
    output_file.write("    end\n\n")

    output_file.write("    wait_state:\n")
    output_file.write("    begin\n")
    output_file.write("      if (timer) begin\n")
    output_file.write("        timer <= timer - 1;\n")
    output_file.write("      end else begin\n")
    output_file.write("        state <= execute;\n")
    output_file.write("      end\n")
    output_file.write("    end\n\n")

    output_file.write("    stop:\n")
    output_file.write("    begin\n")
    output_file.write("    end\n\n")

    for i in floating_point_arithmetic:
        output_file.write("    %s_write_a:\n" % i)
        output_file.write("    begin\n")
        output_file.write("      %s_a_stb <= 1;\n" % i)
        output_file.write("      if (%s_a_stb && %s_a_ack) begin\n" % (i, i))
        output_file.write("        %s_a_stb <= 0;\n" % i)
        output_file.write("        state <= %s_write_b;\n" % i)
        output_file.write("      end\n")
        output_file.write("    end\n\n")
        output_file.write("    %s_write_b:\n" % i)
        output_file.write("    begin\n")
        output_file.write("      %s_b_stb <= 1;\n" % i)
        output_file.write("      if (%s_b_stb && %s_b_ack) begin\n" % (i, i))
        output_file.write("        %s_b_stb <= 0;\n" % i)
        output_file.write("        state <= %s_read_z;\n" % i)
        output_file.write("      end\n")
        output_file.write("    end\n\n")
        output_file.write("    %s_read_z:\n" % i)
        output_file.write("    begin\n")
        output_file.write("      %s_z_ack <= 1;\n" % i)
        output_file.write("      if (%s_z_stb && %s_z_ack) begin\n" % (i, i))
        if i.startswith("double"):
            output_file.write("        a_lo <= %s_z[31:0];\n" % i)
            output_file.write("        a_hi <= %s_z[63:32];\n" % i)
        else:
            output_file.write("        result <= %s_z;\n" % i)
            output_file.write("        write_enable <= 1;\n")
        output_file.write("        %s_z_ack <= 0;\n" % i)
        output_file.write("        state <= execute;\n")
        output_file.write("      end\n")
        output_file.write("    end\n\n")

    for i in floating_point_conversions:
        output_file.write("     %s_write_a:\n" % i)
        output_file.write("     begin\n")
        output_file.write("       %s_in_stb <= 1;\n" % i)
        output_file.write(
            "       if (%s_in_stb && %s_in_ack) begin\n" %
            (i, i))
        output_file.write("         %s_in_stb <= 0;\n" % i)
        output_file.write("         state <= %s_read_z;\n" % i)
        output_file.write("       end\n")
        output_file.write("     end\n\n")
        output_file.write("     %s_read_z:\n" % i)
        output_file.write("     begin\n")
        output_file.write("       %s_out_ack <= 1;\n" % i)
        output_file.write(
            "       if (%s_out_stb && %s_out_ack) begin\n" %
            (i, i))
        output_file.write("         %s_out_ack <= 0;\n" % i)
        if (i.startswith("double") and not i.endswith("float")) or i.endswith("double") or i.startswith("long"):
            output_file.write("         a_lo <= %s_out[31:0];\n" % i)
            output_file.write("         a_hi <= %s_out[63:32];\n" % i)
        else:
            output_file.write("         a_lo <= %s_out;\n" % i)
        output_file.write("         state <= execute;\n")
        output_file.write("       end\n")
        output_file.write("     end\n\n")

    output_file.write("    endcase\n\n")

    # Reset program counter and control signals
    output_file.write("    if (rst == 1'b1) begin\n")
    output_file.write("      timer <= 0;\n")
    output_file.write("      timer_clock <= 0;\n")
    output_file.write("      program_counter <= 0;\n")
    output_file.write("      address_z_3 <= 0;\n")
    output_file.write("      result <= 0;\n")
    output_file.write("      a = 0;\n")
    output_file.write("      b = 0;\n")
    output_file.write("      z = 0;\n")
    output_file.write("      state <= instruction_fetch;\n")

    for i in inputs:
        output_file.write("      s_input_%s_ack <= 0;\n" % (i))

    for i in outputs:
        output_file.write("      s_output_%s_stb <= 0;\n" % (i))

    for i in floating_point_arithmetic:
        output_file.write("      %s_a_stb <= 0;\n" % (i))
        output_file.write("      %s_b_stb <= 0;\n" % (i))
        output_file.write("      %s_z_ack <= 0;\n" % (i))

    for i in floating_point_conversions:
        output_file.write("      %s_in_stb <= 0;\n" % (i))
        output_file.write("      %s_out_ack <= 0;\n" % (i))

    output_file.write("    end\n")
    output_file.write("  end\n")
    for i in inputs:
        output_file.write("  assign input_%s_ack = s_input_%s_ack;\n" % (i, i))
    for i in outputs:
        output_file.write(
            "  assign output_%s_stb = s_output_%s_stb;\n" %
            (i, i))
        output_file.write("  assign output_%s = s_output_%s;\n" % (i, i))
    output_file.write("\nendmodule\n")

    return inputs, outputs
