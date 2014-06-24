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
__version__ = "0.1"

def unique(l):

    """In the absence of set in older python implementations, make list values unique"""

    return dict(zip(l, l)).keys()

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
        return "%s'd%s"%(size, value)
    else:
        return "-%s'd%s"%(size, abs(value))

def generate_instruction_set(instructions):

    """Calculate the required instruction set"""

    instruction_set = []
    instruction_memory = []
    for instruction in instructions:
        opcode = {}
        encoded_instruction = {}
        encoded_instruction["dest"] = 0
        encoded_instruction["src"] = 0
        encoded_instruction["srcb"] = 0
        encoded_instruction["literal"] = 0
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

        if "dest" in instruction:
            encoded_instruction["dest"] = instruction["dest"]

        if "src" in instruction:
            encoded_instruction["src"] = instruction["src"]

        if "srcb" in instruction:
            encoded_instruction["srcb"] = instruction["srcb"]

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


def generate_declarations(instructions, no_tb_mode, register_bits, opcode_bits, allocator):

    """Generate verilog declarations"""

    #list all inputs and outputs used in the program
    inputs = allocator.input_names.values()
    outputs = allocator.output_names.values()
    input_files = unique([i["file_name"] for i in instructions if "file_read" == i["op"]])
    output_files = unique([i["file_name"] for i in instructions if i["op"] in ("file_write", "float_file_write", "long_float_file_write")])
    testbench = not inputs and not outputs and not no_tb_mode

    #Do not generate a port in testbench mode
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

    #create list of signals
    signals = [
      ("timer", 16),
      ("program_counter", log2(len(instructions))),
      ("instruction", 32 + register_bits*2 + opcode_bits),
      ("opcode", opcode_bits),
      ("dest", register_bits),
      ("src", register_bits),
      ("srcb", register_bits),
      ("literal", 32),
      ("register", 32),
      ("registerb", 32),
      ("register_hi", 32),
      ("registerb_hi", 32),
      ("long_result", 64),
      ("result", 32),
      ("result_hi", 32),
      ("write_enable", 1),
      ("address", 16),
      ("data_out", 32),
      ("data_in", 32),
      ("carry", 1),
      ("memory_enable", 1),
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

    floating_point_arithmetic = unique(floating_point_arithmetic)
    floating_point_conversions = unique(floating_point_conversions)
    floating_point_debug = unique(floating_point_debug)

    return floating_point_arithmetic, floating_point_conversions, floating_point_debug

def generate_CHIP(input_file,
                  name,
                  instructions,
                  output_file,
                  registers,
                  allocator,
                  initialize_memory,
                  no_tb_mode=False):

    """A big ugly function to crunch through all the instructions and generate the CHIP equivilent"""

    instructions = calculate_jumps(instructions)
    instruction_set, instruction_memory = generate_instruction_set(instructions)
    register_bits = log2(len(registers));
    opcode_bits = log2(len(instruction_set));
    instruction_bits = 32 + opcode_bits + (2*register_bits)
    assert(32 > 3*register_bits)
    declarations = generate_declarations(instructions, no_tb_mode, register_bits, opcode_bits, allocator)
    inputs, outputs, input_files, output_files, testbench, inports, outports, signals = declarations
    floating_point_arithmetic, floating_point_conversions, floating_point_debug = floating_point_enables(instruction_set)

    #output the code in verilog
    output_file.write("//////////////////////////////////////////////////////////////////////////////\n")
    output_file.write("//name : %s\n"%name)
    for i in inputs:
        output_file.write("//input : input_%s:16\n"%i)
    for i in outputs:
        output_file.write("//output : output_%s:16\n"%i)
    output_file.write("//source_file : %s\n"%input_file)
    output_file.write("///%s\n"%"".join(["=" for i in name]))
    output_file.write("///\n")
    output_file.write("///Created by C2CHIP\n\n")


    output_file.write("//////////////////////////////////////////////////////////////////////////////\n")
    output_file.write("// Register Allocation\n")
    output_file.write("// ===================\n")
    output_file.write("//   %s   %s   %s  \n"%("Register".center(20), "Name".center(20), "Size".center(20)))
    for register, definition in registers.iteritems():
        register_name, size = definition
        output_file.write("//   %s   %s   %s  \n"%(str(register).center(20), register_name.center(20), str(size).center(20)))


    output_file.write("module %s"%name)

    all_ports = [name for name, size in inports + outports]
    if all_ports:
        output_file.write("(")
        output_file.write(",".join(all_ports))
        output_file.write(");\n")
    else:
        output_file.write(";\n")

    output_file.write("  integer file_count;\n")


    for i in floating_point_arithmetic:

        if i.startswith("double"):
            output_file.write("  reg [63:0] %s_a;\n"%(i))
            output_file.write("  reg [63:0] %s_b;\n"%(i))
            output_file.write("  wire [63:0] %s_z;\n"%(i))
        else:
            output_file.write("  reg [31:0] %s_a;\n"%(i))
            output_file.write("  reg [31:0] %s_b;\n"%(i))
            output_file.write("  wire [31:0] %s_z;\n"%(i))

        output_file.write("  reg %s_a_stb;\n"%(i))
        output_file.write("  wire %s_a_ack;\n"%(i))
        output_file.write("  reg %s_b_stb;\n"%(i))
        output_file.write("  wire %s_b_ack;\n"%(i))
        output_file.write("  wire %s_z_stb;\n"%(i))
        output_file.write("  reg %s_z_ack;\n"%(i))

    for i in floating_point_conversions:

        if i.startswith("long") or i.startswith("double"):
            output_file.write("  reg [63:0] %s_in;\n"%(i))
        else:
            output_file.write("  reg [31:0] %s_in;\n"%(i))

        if i.endswith("long") or i.endswith("double"):
            output_file.write("  wire [63:0] %s_out;\n"%(i))
        else:
            output_file.write("  wire [31:0] %s_out;\n"%(i))

        output_file.write("  wire %s_out_stb;\n"%(i))
        output_file.write("  reg %s_out_ack;\n"%(i))
        output_file.write("  reg %s_in_stb;\n"%(i))
        output_file.write("  wire %s_in_ack;\n"%(i))

    if floating_point_debug:
        output_file.write("  real fp_value;\n")

    states = ["stop", "instruction_fetch", "instruction_decode", "opcode_fetch", "execute", "wait_state"]

    memory_size = int(allocator.memory_size)
    if memory_size:
        states.append("read_memory_wait")
        states.append("read_memory")

    if inports:
        states.append("read")

    if outports:
        states.append("write")

    for i in floating_point_arithmetic:
        states.append("%s_write_a"%i)
        states.append("%s_write_b"%i)
        states.append("%s_read_z"%i)

    for i in floating_point_conversions:
        states.append("%s_write_a"%i)
        states.append("%s_read_z"%i)

    state_variables = []
    for index, state in enumerate(states):
        state_variables.append("%s = %s'd%s"%(state, log2(len(states)), index))

    signals.append(("state", len(state_variables)))
    output_file.write("  parameter  ")
    output_file.write(",\n  ".join(state_variables))
    output_file.write(";\n")

    input_files = dict(zip(input_files, ["input_file_%s"%i for i, j in enumerate(input_files)]))
    for i in input_files.values():
        output_file.write("  integer %s;\n"%i)

    output_files = dict(zip(output_files, ["output_file_%s"%i for i, j in enumerate(output_files)]))
    for i in output_files.values():
        output_file.write("  integer %s;\n"%i)


    def write_declaration(object_type, name, size):
        if size == 1:
            output_file.write(object_type)
            output_file.write(name)
            output_file.write(";\n")
        else:
            output_file.write(object_type)
            output_file.write("[%i:0]"%(size-1))
            output_file.write(" ")
            output_file.write(name)
            output_file.write(";\n")

    for name, size in inports:
        write_declaration("  input ", name, size)

    for name, size in outports:
        write_declaration("  output ", name, size)

    for name, size in signals:
        write_declaration("  reg ", name, size)

    if memory_size:
        output_file.write("  reg [31:0] memory [%i:0];\n"%(memory_size-1))

    output_file.write("  reg [%s:0] instructions [%i:0];\n"%(instruction_bits-1, len(instructions)-1))
    output_file.write("  reg [31:0] registers [%i:0];\n"%(len(registers)-1))


    #generate clock and reset in testbench mode
    if testbench:

        output_file.write("\n  //////////////////////////////////////////////////////////////////////////////\n")
        output_file.write("  // CLOCK AND RESET GENERATION                                                 \n")
        output_file.write("  //                                                                            \n")
        output_file.write("  // This file was generated in test bench mode. In this mode, the verilog      \n")
        output_file.write("  // output file can be executed directly within a verilog simulator.           \n")
        output_file.write("  // In test bench mode, a simulated clock and reset signal are generated within\n")
        output_file.write("  // the output file.                                                           \n")
        output_file.write("  // Verilog files generated in testbecnch mode are not suitable for synthesis, \n")
        output_file.write("  // or for instantiation within a larger design.\n")

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

    #Instance Floating Point Arithmetic
    if floating_point_arithmetic or floating_point_conversions:

        output_file.write("\n  //////////////////////////////////////////////////////////////////////////////\n")
        output_file.write("  // Floating Point Arithmetic                                                  \n")
        output_file.write("  //                                                                            \n")
        output_file.write("  // Generate IEEE 754 single precision divider, adder and multiplier           \n")
        output_file.write("  //                                                                            \n")

        for i in floating_point_arithmetic:
            output_file.write("  %s %s_inst(\n"%(i, i))
            output_file.write("    .clk(clk),\n")
            output_file.write("    .rst(rst),\n")
            output_file.write("    .input_a(%s_a),\n"%i)
            output_file.write("    .input_a_stb(%s_a_stb),\n"%i)
            output_file.write("    .input_a_ack(%s_a_ack),\n"%i)
            output_file.write("    .input_b(%s_b),\n"%i)
            output_file.write("    .input_b_stb(%s_b_stb),\n"%i)
            output_file.write("    .input_b_ack(%s_b_ack),\n"%i)
            output_file.write("    .output_z(%s_z),\n"%i)
            output_file.write("    .output_z_stb(%s_z_stb),\n"%i)
            output_file.write("    .output_z_ack(%s_z_ack)\n"%i)
            output_file.write("  );\n")

        for i in floating_point_conversions:
            output_file.write("  %s %s_inst(\n"%(i, i))
            output_file.write("    .clk(clk),\n")
            output_file.write("    .rst(rst),\n")
            output_file.write("    .input_a(%s_in),\n"%i)
            output_file.write("    .input_a_stb(%s_in_stb),\n"%i)
            output_file.write("    .input_a_ack(%s_in_ack),\n"%i)
            output_file.write("    .output_z(%s_out),\n"%i)
            output_file.write("    .output_z_stb(%s_out_stb),\n"%i)
            output_file.write("    .output_z_ack(%s_out_ack)\n"%i)
            output_file.write("  );\n")


    #Generate a state machine to execute the instructions
    if initialize_memory and allocator.memory_content:

        output_file.write("\n  //////////////////////////////////////////////////////////////////////////////\n")
        output_file.write("  // MEMORY INITIALIZATION                                                      \n")
        output_file.write("  //                                                                            \n")
        output_file.write("  // In order to reduce program size, array contents have been stored into      \n")
        output_file.write("  // memory at initialization. In an FPGA, this will result in the memory being \n")
        output_file.write("  // initialized when the FPGA configures.                                      \n")
        output_file.write("  // Memory will not be re-initialized at reset.                                \n")
        output_file.write("  // Dissable this behaviour using the no_initialize_memory switch              \n")

        output_file.write("  \n  initial\n")
        output_file.write("  begin\n")
        for location, content in allocator.memory_content.iteritems():
            output_file.write("    memory[%s] = %s;\n"%(location, content))
        output_file.write("  end\n\n")


    output_file.write("\n  //////////////////////////////////////////////////////////////////////////////\n")
    output_file.write("  // INSTRUCTION INITIALIZATION                                                 \n")
    output_file.write("  //                                                                            \n")
    output_file.write("  // Initialise the contents of the instruction memory                          \n")
    output_file.write("  //\n")
    output_file.write("  // Intruction Set\n")
    output_file.write("  // ==============\n")
    for num, opcode in enumerate(instruction_set):
        output_file.write("  // %s %s\n"%(num, opcode))

    output_file.write("  // Intructions\n")
    output_file.write("  // ===========\n")
    output_file.write("  \n  initial\n")
    output_file.write("  begin\n")
    for location, instruction in enumerate(instruction_memory):
        output_file.write("    instructions[%s] = {%s, %s, %s, %s};//%s\n"%(
            location,
            print_verilog_literal(opcode_bits, instruction["op"]),
            print_verilog_literal(register_bits, instruction["dest"]),
            print_verilog_literal(register_bits, instruction["src"]),
            print_verilog_literal(32, instruction["srcb"] | instruction["literal"]),
            instruction["comment"]))
    output_file.write("  end\n\n")

    if input_files or output_files:

        output_file.write("\n  //////////////////////////////////////////////////////////////////////////////\n")
        output_file.write("  // OPEN FILES                                                                 \n")
        output_file.write("  //                                                                            \n")
        output_file.write("  // Open all files used at the start of the process                            \n")

        output_file.write("  \n  initial\n")
        output_file.write("  begin\n")
        for file_name, file_ in input_files.iteritems():
            output_file.write("    %s = $fopenr(\"%s\");\n"%(file_, file_name))
        for file_name, file_ in output_files.iteritems():
            output_file.write("    %s = $fopen(\"%s\");\n"%(file_, file_name))
        output_file.write("  end\n\n")

    if memory_size:
        output_file.write("\n  //////////////////////////////////////////////////////////////////////////////\n")
        output_file.write("  // DATA MEMORY\n")
        output_file.write("  //                                                                            \n")
        output_file.write("  \n  always @(posedge clk)\n")
        output_file.write("  begin\n\n")
        output_file.write("    //implement memory for 4 byte x n arrays\n")
        output_file.write("    if (memory_enable == 1'b1) begin\n")
        output_file.write("      memory[address] <= data_in;\n")
        output_file.write("    end\n")
        output_file.write("    data_out <= memory[address];\n")
        output_file.write("  end\n\n")

    output_file.write("\n  //////////////////////////////////////////////////////////////////////////////\n")
    output_file.write("  // INSTRUCTION MEMORY\n")
    output_file.write("  //                                                                            \n")
    output_file.write("  \n  always @(posedge clk)\n")
    output_file.write("  begin\n\n")
    output_file.write("    //implement memory for instructions\n")
    output_file.write("    instruction <= instructions[program_counter];\n")
    output_file.write("  end\n\n")

    output_file.write("\n  //////////////////////////////////////////////////////////////////////////////\n")
    output_file.write("  // CPU IMPLEMENTAION OF C PROCESS                                             \n")
    output_file.write("  //                                                                            \n")
    output_file.write("  // This section of the file contains a CPU implementing the C process.        \n")

    output_file.write("  \n  always @(posedge clk)\n")
    output_file.write("  begin\n\n")
    #output_file.write("    $display(state);\n\n")
    #output_file.write("    $display(program_counter);\n\n")
    output_file.write("    memory_enable <= 1'b0;\n\n")
    output_file.write("  case(state)\n\n")
    output_file.write("    //instruction fetch\n")
    output_file.write("    instruction_fetch:\n")
    output_file.write("    begin\n")
    output_file.write("      //wait for instruction read;\n")
    output_file.write("      state <= instruction_decode;\n")
    output_file.write("    end\n\n")

    output_file.write("    //instruction decode\n")
    output_file.write("    instruction_decode:\n")
    output_file.write("    begin\n")
    output_file.write("      opcode <= instruction[%s:%s];\n"%(
        instruction_bits - 1,
        instruction_bits - opcode_bits))
    output_file.write("      dest <= instruction[%s:%s];\n"%(
        register_bits * 2 + 32 - 1,
        register_bits * 1 + 32))
    output_file.write("      src <= instruction[%s:%s];\n"%(
        register_bits * 1 + 32 - 1,
        32))
    output_file.write("      srcb <= instruction[%s:0];\n"%(register_bits-1))
    output_file.write("      literal <= instruction[31:0];\n")
    output_file.write("      if(write_enable) begin\n")
    output_file.write("            registers[dest] <= result;\n")
    output_file.write("      end\n")
    output_file.write("      state <= opcode_fetch;\n")
    output_file.write("      program_counter <= program_counter + 1;\n")
    output_file.write("    end\n\n")

    output_file.write("    //opcode fetch\n")
    output_file.write("    opcode_fetch:\n")
    output_file.write("    begin\n")
    output_file.write("      register <= registers[src];\n")
    output_file.write("      registerb <= registers[srcb];\n")
    output_file.write("      state <= execute;\n")
    output_file.write("    end\n\n")

    output_file.write("    //execute\n")
    output_file.write("    execute: begin\n")
    output_file.write("      state <= execute;\n")
    output_file.write("      write_enable <= 0;\n")
    output_file.write("      state <= instruction_decode;\n")
    output_file.write("      case(opcode)\n\n")

    #A frame is executed in each state
    for opcode, instruction in enumerate(instruction_set):

        output_file.write("        //%s\n"%(instruction["op"]))
        output_file.write("        16'd%s:\n"%(opcode))
        output_file.write("        begin\n")

        if instruction["op"] == "nop":
            pass

        elif instruction["op"] == "literal":
            output_file.write("          result <= literal;\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "move":
            output_file.write("          result <= register;\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "not":
            output_file.write("          result <= ~register;\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "int_to_float":
            output_file.write("          int_to_float_in <= register;\n")
            output_file.write("          state <= int_to_float_write_a;\n")

        elif instruction["op"] == "float_to_int":
            output_file.write("          float_to_int_in <= register;\n")
            output_file.write("          state <= float_to_int_write_a;\n")

        elif instruction["op"] == "long_to_double":
            output_file.write("          long_to_double_in <= {register_hi, register};\n")
            output_file.write("          state <= long_to_double_write_a;\n")

        elif instruction["op"] == "double_to_long":
            output_file.write("          double_to_long_in <= {register_hi, register};\n")
            output_file.write("          state <= double_to_long_write_a;\n")

        elif instruction["op"] == "float_to_double":
            output_file.write("          float_to_double_in <= {register_hi, register};\n")
            output_file.write("          state <= float_to_double_write_a;\n")

        elif instruction["op"] == "double_to_float":
            output_file.write("          double_to_float_in <= {register_hi, register};\n")
            output_file.write("          state <= double_to_float_write_a;\n")

        elif instruction["op"] == "load_hi":
            output_file.write("          register_hi <= register;\n")
            output_file.write("          registerb_hi <= registerb;\n")

        elif instruction["op"] == "add":
            output_file.write("          long_result = register + registerb;\n")
            output_file.write("          result <= long_result[31:0];\n")
            output_file.write("          carry <= long_result[32];\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "add_with_carry":
            output_file.write("          long_result = register + registerb + carry;\n")
            output_file.write("          result <= long_result[31:0];\n")
            output_file.write("          carry <= long_result[32];\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "subtract":
            output_file.write("          long_result = register + (~registerb) + 1;\n")
            output_file.write("          result <= long_result[31:0];\n")
            output_file.write("          carry <= ~long_result[32];\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "subtract_with_carry":
            output_file.write("          long_result = register + (~registerb) + carry;\n")
            output_file.write("          result <= long_result[31:0];\n")
            output_file.write("          carry <= ~long_result[32];\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "multiply":
            output_file.write("          long_result = register * registerb;\n")
            output_file.write("          result <= long_result[31:0];\n")
            output_file.write("          result_hi <= long_result[63:32];\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "result_hi":
            output_file.write("          result <= result_hi;\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "or":
            output_file.write("          result <= register | registerb;\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "and":
            output_file.write("          result <= register & registerb;\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "xor":
            output_file.write("          result <= register ^ registerb;\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "shift_left":
            output_file.write("          result <= {register[30:0], 1'd0};\n")
            output_file.write("          carry <= register[31];\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "shift_left_with_carry":
            output_file.write("          result <= {register[30:0], carry};\n")
            output_file.write("          carry <= register[31];\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "shift_right":
            output_file.write("          result <= {register[31], register[31:1]};\n")
            output_file.write("          carry <= register[0];\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "unsigned_shift_right":
            output_file.write("          result <= {1'd0, register[31:1]};\n")
            output_file.write("          carry <= register[0];\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "shift_right_with_carry":
            output_file.write("          result = {carry, register[31:1]};\n")
            output_file.write("          carry <= register[0];\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "greater":
            output_file.write("          result <= $signed(register) > $signed(registerb);\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "greater_equal":
            output_file.write("          result <= $signed(register) >= $signed(registerb);\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "unsigned_greater":
            output_file.write("          result <= $unsigned(register) > $unsigned(registerb);\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "unsigned_greater_equal":
            output_file.write("          result <= $unsigned(register) >= $unsigned(registerb);\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "equal":
            output_file.write("          result <= register == registerb;\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "not_equal":
            output_file.write("          result <= register != registerb;\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "float_add":
            output_file.write("          adder_a <= register;\n")
            output_file.write("          adder_b <= registerb;\n")
            output_file.write("          state <= adder_write_a;\n")

        elif instruction["op"] == "float_subtract":
            output_file.write("          adder_a <= register;\n")
            output_file.write("          adder_b <= {~registerb[31], registerb[30:0]};\n")
            output_file.write("          state <= adder_write_a;\n")

        elif instruction["op"] == "float_multiply":
            output_file.write("          multiplier_a <= register;\n")
            output_file.write("          multiplier_b <= registerb;\n")
            output_file.write("          state <= multiplier_write_a;\n")

        elif instruction["op"] == "float_divide":
            output_file.write("          divider_a <= register;\n")
            output_file.write("          divider_b <= registerb;\n")
            output_file.write("          state <= divider_write_a;\n")

        elif instruction["op"] == "long_float_add":
            output_file.write("          double_adder_a <= {register_hi, register};\n")
            output_file.write("          double_adder_b <= {registerb_hi, registerb};\n")
            output_file.write("          state <= double_adder_write_a;\n")

        elif instruction["op"] == "long_float_subtract":
            output_file.write("          double_adder_a <= {register_hi, register};\n")
            output_file.write("          double_adder_b <= {~registerb_hi[31], registerb_hi[30:0], registerb};\n")
            output_file.write("          state <= double_adder_write_a;\n")

        elif instruction["op"] == "long_float_multiply":
            output_file.write("          double_multiplier_a <= {register_hi, register};\n")
            output_file.write("          double_multiplier_b <= {registerb_hi, registerb};\n")
            output_file.write("          state <= double_multiplier_write_a;\n")

        elif instruction["op"] == "long_float_divide":
            output_file.write("          double_divider_a <= {register_hi, register};\n")
            output_file.write("          double_divider_b <= {registerb_hi, registerb};\n")
            output_file.write("          state <= double_divider_write_a;\n")

        elif instruction["op"] == "jmp_if_false":
            output_file.write("          if (register == 0) begin\n");
            output_file.write("            program_counter <= literal;\n")
            output_file.write("            state <= instruction_fetch;\n")
            output_file.write("          end\n")

        elif instruction["op"] == "jmp_if_true":
            output_file.write("          if (register != 0) begin\n");
            output_file.write("            program_counter <= literal;\n")
            output_file.write("            state <= instruction_fetch;\n")
            output_file.write("          end\n")

        elif instruction["op"] == "jmp_and_link":
            output_file.write("          program_counter <= literal;\n")
            output_file.write("          state <= instruction_fetch;\n")
            output_file.write("          result <= program_counter;\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "jmp_to_reg":
            output_file.write("          program_counter <= register;\n")
            output_file.write("          state <= instruction_fetch;\n")

        elif instruction["op"] == "goto":
            output_file.write("          program_counter <= literal;\n")
            output_file.write("          state <= instruction_fetch;\n")

        elif instruction["op"] == "file_read":
            output_file.write("        16'd%s:\n"%(opcode))
            output_file.write("        begin\n")
            output_file.write("          file_count = $fscanf(%s, \"%%d\\n\", result);\n"%(
              input_files[instruction["file_name"]]))
            output_file.write("          write_enable <= 1;\n")
            output_file.write("        end\n\n")

        elif instruction["op"] == "float_file_write":
            output_file.write('          long_result[63] = register[31];\n')
            output_file.write('          if (register[30:23] == 0) begin\n')
            output_file.write('              long_result[62:52] = 0;\n')
            output_file.write('          end else if (register[30:23] == 127) begin\n')
            output_file.write('              long_result[62:52] = 1023;\n')
            output_file.write('          end else begin\n')
            output_file.write('              long_result[62:52] = (register[30:23] - 127) + 1023;\n')
            output_file.write('          end\n')
            output_file.write('          long_result[51:29] = register[22:0];\n')
            output_file.write('          long_result[28:0] = 0;\n')
            output_file.write('          fp_value = $bitstoreal(long_result);\n')
            output_file.write('          $fdisplay (%s, "%%g", fp_value);\n'%(
                  output_files[
                  instruction["file_name"]]))

        elif instruction["op"] == "long_float_file_write":
            output_file.write('          fp_value = $bitstoreal({register_hi, register});\n')
            output_file.write('          $fdisplay (%s, "%%g", fp_value);\n'%(
                  output_files[
                  instruction["file_name"]]))

        elif instruction["op"] == "unsigned_file_write":
            output_file.write("          $fdisplay (%s, \"%%d\", $unsigned(register));\n"%(
            output_files[instruction["file_name"]]))

        elif instruction["op"] == "file_write":
            output_file.write("          $fdisplay (%s, \"%%d\", $signed(register));\n"%(
            output_files[instruction["file_name"]]))

        elif instruction["op"] == "read":
            output_file.write("          state <= read;\n")

        elif instruction["op"] == "ready":
            output_file.write("          result <= 0;\n")
            output_file.write("          case(register)\n\n")
            for handle, input_name in allocator.input_names.iteritems():
                output_file.write("            %s:\n"%(handle))
                output_file.write("            begin\n")
                output_file.write("              result[0] <= s_input_%s_ack;\n"%input_name)
                output_file.write("            end\n")
            output_file.write("          endcase\n")
            output_file.write("          write_enable <= 1;\n")

        elif instruction["op"] == "write":
            output_file.write("          state <= write;\n")

        elif instruction["op"] == "memory_read":
            output_file.write("          address <= register;\n")
            output_file.write("          state <= read_memory_wait;\n")

        elif instruction["op"] == "memory_write":
            output_file.write("          address <= register;\n")
            output_file.write("          data_in <= registerb;\n")
            output_file.write("          memory_enable <= 1'b1;\n")

        elif instruction["op"] == "assert":
            output_file.write("          if (register == 0) begin\n")
            output_file.write("            $display(\"Assertion failed at line: %s in file: %s\");\n"%(
              instruction["line"],
              instruction["file"]))
            output_file.write("            $finish_and_return(1);\n")
            output_file.write("          end\n")

        elif instruction["op"] == "wait_clocks":
            output_file.write("          timer <= register;\n")
            output_file.write("          state <= wait_state;\n")

        elif instruction["op"] == "report":
            output_file.write('          $display ("%%d (report (int) at line: %s in file: %s)", $signed(register));\n'%(
                instruction["line"],
                instruction["file"],))

        elif instruction["op"] == "long_report":
            output_file.write('          $display ("%%d (report (long) at line: %s in file: %s)", $signed({register_hi, register}));\n'%(
                instruction["line"],
                instruction["file"],))

        elif instruction["op"] == "float_report":
           output_file.write('          long_result[63] = register[31];\n')
           output_file.write('          if (register[30:23] == 0) begin\n')
           output_file.write('              long_result[62:52] = 0;\n')
           output_file.write('          end else if (register[30:23] == 127) begin\n')
           output_file.write('              long_result[62:52] = 1023;\n')
           output_file.write('          end else begin\n')
           output_file.write('              long_result[62:52] = (register[30:23] - 127) + 1023;\n')
           output_file.write('          end\n')
           output_file.write('          long_result[51:29] = register[22:0];\n')
           output_file.write('          long_result[28:0] = 0;\n')
           output_file.write('          fp_value = $bitstoreal(long_result);\n')
           output_file.write('          $display ("%%g (report (float) at line: %s in file: %s)", fp_value);\n'%(
                  instruction["line"],
                  instruction["file"]))

        elif instruction["op"] == "long_float_report":
           output_file.write('          fp_value = $bitstoreal({register_hi, register});\n')
           output_file.write('          $display ("%%g (report (double) at line: %s in file: %s)", fp_value);\n'%(
                  instruction["line"],
                  instruction["file"]))

        elif instruction["op"] == "unsigned_report":
           output_file.write('          $display ("%%d (report (unsigned) at line: %s in file: %s)", $unsigned(register));\n'%(
	       instruction["line"],
	       instruction["file"]))

        elif instruction["op"] == "long_unsigned_report":
           output_file.write('          $display ("%%d (report (unsigned long) at line: %s in file: %s)", $unsigned({register_hi, register}));\n'%(
	       instruction["line"],
	       instruction["file"]))

        elif instruction["op"] == "stop":
            #If we are in testbench mode stop the simulation
            #If we are part of a larger design, other C programs may still be running
            for file_ in input_files.values():
                output_file.write("          $fclose(%s);\n"%file_)
            for file_ in output_files.values():
                output_file.write("          $fclose(%s);\n"%file_)
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
        output_file.write("      case(register)\n")
        for handle, input_name in allocator.input_names.iteritems():
            output_file.write("      %s:\n"%(handle))
            output_file.write("      begin\n")
            output_file.write("        s_input_%s_ack <= 1;\n"%input_name)
            output_file.write("        if (s_input_%s_ack && input_%s_stb) begin\n"%(
              input_name,
              input_name))
            output_file.write("          result <= input_%s;\n"%input_name)
            output_file.write("          write_enable <= 1;\n")
            output_file.write("          s_input_%s_ack <= 0;\n"%input_name)
            output_file.write("          state <= instruction_decode;\n")
            output_file.write("        end\n")
            output_file.write("      end\n")
        output_file.write("      endcase\n")
        output_file.write("    end\n\n")

    if allocator.output_names:
        output_file.write("    write:\n")
        output_file.write("    begin\n")
        output_file.write("      case(register)\n")
        for handle, output_name in allocator.output_names.iteritems():
            output_file.write("      %s:\n"%(handle))
            output_file.write("      begin\n")
            output_file.write("        s_output_%s_stb <= 1;\n"%output_name)
            output_file.write("        s_output_%s <= registerb;\n"%output_name)
            output_file.write("        if (output_%s_ack && s_output_%s_stb) begin\n"%(
              output_name,
              output_name))
            output_file.write("          s_output_%s_stb <= 0;\n"%output_name)
            output_file.write("          state <= instruction_decode;\n")
            output_file.write("        end\n")
            output_file.write("      end\n")
        output_file.write("      endcase\n")
        output_file.write("    end\n\n")
 
    output_file.write("    wait_state:\n")
    output_file.write("    begin\n")
    output_file.write("      if (timer) begin\n")
    output_file.write("        timer <= timer - 1;\n")
    output_file.write("      end else begin\n")
    output_file.write("        state <= instruction_decode;\n")
    output_file.write("      end\n")
    output_file.write("    end\n\n")

    output_file.write("    stop:\n")
    output_file.write("    begin\n")
    output_file.write("    end\n\n")

    if memory_size:
        output_file.write("    read_memory_wait:\n")
        output_file.write("    begin\n")
        output_file.write("      state <= read_memory;\n")
        output_file.write("    end\n\n")

        output_file.write("    read_memory:\n")
        output_file.write("    begin\n")
        output_file.write("      result <= data_out;\n")
        output_file.write("      write_enable <= 1;\n")
        output_file.write("      state <= instruction_decode;\n")
        output_file.write("    end\n\n")

    for i in floating_point_arithmetic:
        output_file.write("    %s_write_a:\n"%i)
        output_file.write("    begin\n")
        output_file.write("      %s_a_stb <= 1;\n"%i)
        output_file.write("      if (%s_a_stb && %s_a_ack) begin\n"%(i, i))
        output_file.write("        %s_a_stb <= 0;\n"%i)
        output_file.write("        state <= %s_write_b;\n"%i)
        output_file.write("      end\n")
        output_file.write("    end\n\n")
        output_file.write("    %s_write_b:\n"%i)
        output_file.write("    begin\n")
        output_file.write("      %s_b_stb <= 1;\n"%i)
        output_file.write("      if (%s_b_stb && %s_b_ack) begin\n"%(i, i))
        output_file.write("        %s_b_stb <= 0;\n"%i)
        output_file.write("        state <= %s_read_z;\n"%i)
        output_file.write("      end\n")
        output_file.write("    end\n\n")
        output_file.write("    %s_read_z:\n"%i)
        output_file.write("    begin\n")
        output_file.write("      %s_z_ack <= 1;\n"%i)
        output_file.write("      if (%s_z_stb && %s_z_ack) begin\n"%(i, i))
        if i.startswith("double"):
            output_file.write("        result <= %s_z[31:0];\n"%i)
            output_file.write("        result_hi <= %s_z[63:32];\n"%i)
        else:
            output_file.write("        result <= %s_z;\n"%i)
        output_file.write("        write_enable <= 1;\n")
        output_file.write("        %s_z_ack <= 0;\n"%i)
        output_file.write("        state <= instruction_decode;\n")
        output_file.write("      end\n")
        output_file.write("    end\n\n")

    for i in floating_point_conversions:
        output_file.write("     %s_write_a:\n"%i)
        output_file.write("     begin\n")
        output_file.write("       %s_in_stb <= 1;\n"%i)
        output_file.write("       if (%s_in_stb && %s_in_ack) begin\n"%(i,i))
        output_file.write("         %s_in_stb <= 0;\n"%i)
        output_file.write("         state <= %s_read_z;\n"%i)
        output_file.write("       end\n")
        output_file.write("     end\n\n")
        output_file.write("     %s_read_z:\n"%i)
        output_file.write("     begin\n")
        output_file.write("       %s_out_ack <= 1;\n"%i)
        output_file.write("       if (%s_out_stb && %s_out_ack) begin\n"%(i,i))
        output_file.write("         %s_out_ack <= 0;\n"%i)
        if i.startswith("double") or i.startswith("long"):
            output_file.write("         result <= %s_out[31:0];\n"%i)
            output_file.write("         result_hi <= %s_out[63:32];\n"%i)
        else:
            output_file.write("         result <= %s_out;\n"%i)
        output_file.write("         write_enable <= 1;\n")
        output_file.write("         state <= instruction_decode;\n")
        output_file.write("       end\n")
        output_file.write("     end\n\n")

    output_file.write("    endcase\n\n")

    #Reset program counter and control signals
    output_file.write("    if (rst == 1'b1) begin\n")
    output_file.write("      timer <= 0;\n")
    output_file.write("      program_counter <= 0;\n")
    output_file.write("      state <= instruction_fetch;\n")

    for i in inputs:
        output_file.write("      s_input_%s_ack <= 0;\n"%(i))

    for i in outputs:
        output_file.write("      s_output_%s_stb <= 0;\n"%(i))

    for i in floating_point_arithmetic:
        output_file.write("      %s_a_stb <= 0;\n"%(i))
        output_file.write("      %s_b_stb <= 0;\n"%(i))
        output_file.write("      %s_z_ack <= 0;\n"%(i))

    for i in floating_point_conversions:
        output_file.write("      %s_in_stb <= 0;\n"%(i))
        output_file.write("      %s_out_ack <= 0;\n"%(i))

    output_file.write("    end\n")
    output_file.write("  end\n")
    for i in inputs:
        output_file.write("  assign input_%s_ack = s_input_%s_ack;\n"%(i, i))
    for i in outputs:
        output_file.write("  assign output_%s_stb = s_output_%s_stb;\n"%(i, i))
        output_file.write("  assign output_%s = s_output_%s;\n"%(i, i))
    output_file.write("\nendmodule\n")

    return inputs, outputs

