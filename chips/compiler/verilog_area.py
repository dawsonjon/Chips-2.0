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

def remove_register_hazards(instructions):

    """search through instructions, and remove register hazards"""

    wait_2_for = None
    wait_1_for = None
    new_instructions = []
    for instruction in instructions:
        wait = 0
        if "src" in instruction:
            if instruction["src"] == wait_1_for:
                wait = max(wait, 1)
            if instruction["src"] == wait_2_for:
                wait = max(wait, 2)
        if "srcb" in instruction:
            if instruction["srcb"] == wait_1_for:
                wait = max(wait, 1)
            if instruction["srcb"] == wait_2_for:
                wait = max(wait, 2)
        for i in range(wait):
            new_instructions.append({"op":"nop"})
        new_instructions.append(instruction)

        if instruction["op"] != "label":
            wait_1_for = wait_2_for
            if "dest" in instruction:
                wait_2_for = instruction["dest"]
            else:
                wait_2_for = None
    return new_instructions

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
    output_files = unique([i["file_name"] for i in instructions if "file_write" == i["op"]])
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
      ("timer_enable", 1),
      ("stage_0_enable", 1),
      ("stage_1_enable", 1),
      ("stage_2_enable", 1),
      ("program_counter", log2(len(instructions))),
      ("program_counter_0", log2(len(instructions))),
      ("instruction_0", 32 + register_bits*2 + opcode_bits),
      ("opcode_0", opcode_bits),
      ("dest_0", register_bits),
      ("src_0", register_bits),
      ("srcb_0", register_bits),
      ("literal_0", 32),
      ("program_counter_1", log2(len(instructions))),
      ("opcode_1", opcode_bits),
      ("dest_1", register_bits),
      ("register_1", 32),
      ("registerb_1", 32),
      ("register_hi_1", 32),
      ("registerb_hi_1", 32),
      ("literal_1", 32),
      ("dest_2", register_bits),
      ("long_result", 64),
      ("result_2", 32),
      ("result_hi_2", 32),
      ("write_enable_2", 1),
      ("write_enable_hi_2", 1),
      ("address", 16),
      ("data_out", 32),
      ("data_in", 32),
      ("carry", 1),
      ("result_hi", 32),
      ("register_hi", 32),
      ("registerb_hi", 32),
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
    enable_adder = False
    enable_multiplier = False
    enable_divider = False
    enable_long_adder = False
    enable_long_multiplier = False
    enable_long_divider = False
    enable_int_to_float = False
    enable_float_to_int = False
    enable_long_to_double = False
    enable_double_to_long = False
    enable_float_to_double = False
    enable_double_to_float = False
    for i in instruction_set:
        if i["op"] == "float_add":
            enable_adder = True
        if i["op"] == "float_subtract":
            enable_adder = True
        if i["op"] == "float_multiply":
            enable_multiplier = True
        if i["op"] == "float_divide":
            enable_divider = True
        if i["op"] == "long_float_add":
            enable_long_adder = True
        if i["op"] == "long_float_subtract":
            enable_long_adder = True
        if i["op"] == "long_float_multiply":
            enable_long_multiplier = True
        if i["op"] == "long_float_divide":
            enable_long_divider = True
        if i["op"] == "int_to_float":
            enable_int_to_float = True
        if i["op"] == "float_to_int":
            enable_float_to_int = True
        if i["op"] == "long_to_double":
            enable_long_to_double = True
        if i["op"] == "double_to_long":
            enable_double_to_long = True
        if i["op"] == "float_to_double":
            enable_float_to_double = True
        if i["op"] == "double_to_float":
            enable_double_to_float = True

    return (
        enable_adder, 
        enable_multiplier, 
        enable_divider, 
        enable_long_adder, 
        enable_long_multiplier, 
        enable_long_divider, 
        enable_long_to_double,
        enable_double_to_long,
        enable_float_to_double,
        enable_double_to_float,
        enable_int_to_float, 
        enable_float_to_int)

def generate_CHIP(input_file,
                  name,
                  instructions,
                  output_file,
                  registers,
                  allocator,
                  initialize_memory,
                  no_tb_mode=False):

    """A big ugly function to crunch through all the instructions and generate the CHIP equivilent"""

    instructions = remove_register_hazards(instructions)
    instructions = calculate_jumps(instructions)
    instruction_set, instruction_memory = generate_instruction_set(instructions)
    register_bits = log2(len(registers));
    opcode_bits = log2(len(instruction_set));
    instruction_bits = 32 + register_bits*2 + opcode_bits
    declarations = generate_declarations(instructions, no_tb_mode, register_bits, opcode_bits, allocator)
    inputs, outputs, input_files, output_files, testbench, inports, outports, signals = declarations

    (
    enable_adder, 
    enable_multiplier, 
    enable_divider,  
    enable_long_adder, 
    enable_long_multiplier, 
    enable_long_divider, 
    enable_long_to_double, 
    enable_double_to_long, 
    enable_float_to_double, 
    enable_double_to_float, 
    enable_int_to_float, 
    enable_float_to_int
    ) = floating_point_enables(instruction_set)

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


    if enable_adder:
        generate_adder_signals(output_file)
    if enable_multiplier:
        generate_multiplier_signals(output_file)
    if enable_divider:
        generate_divider_signals(output_file)
    if enable_long_adder:
        generate_long_adder_signals(output_file)
    if enable_long_multiplier:
        generate_long_multiplier_signals(output_file)
    if enable_long_divider:
        generate_long_divider_signals(output_file)
    if enable_int_to_float:
        generate_int_to_float_signals(output_file)
    if enable_float_to_int:
        generate_float_to_int_signals(output_file)
    if enable_long_to_double:
        generate_long_to_double_signals(output_file)
    if enable_float_to_double:
        generate_float_to_double_signals(output_file)
    if enable_double_to_long:
        generate_double_to_long_signals(output_file)
    if enable_double_to_float:
        generate_double_to_float_signals(output_file)

    output_file.write("  real fp_value;\n")
    if (enable_adder or enable_multiplier or enable_divider or 
        enable_long_adder or enable_long_multiplier or enable_long_divider or 
        enable_float_to_double or enable_double_to_float or
        enable_long_to_double or enable_double_to_long or enable_int_to_float or
        enable_float_to_int):
        output_file.write("  parameter wait_go = 2'd0,\n")
        output_file.write("            write_a = 2'd1,\n")
        output_file.write("            write_b = 2'd2,\n")
        output_file.write("            read_z  = 2'd3;\n")
    

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

    memory_size = int(allocator.memory_size)
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
    if (enable_adder or enable_multiplier or enable_divider or 
        enable_long_adder or enable_long_multiplier or enable_long_divider or 
        enable_float_to_double or enable_double_to_float or
        enable_long_to_double or enable_double_to_long or enable_int_to_float or
        enable_float_to_int):

        output_file.write("\n  //////////////////////////////////////////////////////////////////////////////\n")
        output_file.write("  // Floating Point Arithmetic                                                  \n")
        output_file.write("  //                                                                            \n")
        output_file.write("  // Generate IEEE 754 single precision divider, adder and multiplier           \n")
        output_file.write("  //                                                                            \n")

        if enable_divider:
            connect_divider(output_file)
        if enable_multiplier:
            connect_multiplier(output_file)
        if enable_adder:
            connect_adder(output_file)
        if enable_long_divider:
            connect_long_divider(output_file)
        if enable_long_multiplier:
            connect_long_multiplier(output_file)
        if enable_long_adder:
            connect_long_adder(output_file)
        if enable_long_to_double:
            connect_long_to_double(output_file)
        if enable_double_to_long:
            connect_double_to_long(output_file)
        if enable_float_to_double:
            connect_float_to_double(output_file)
        if enable_double_to_float:
            connect_double_to_float(output_file)
        if enable_int_to_float:
            connect_int_to_float(output_file)
        if enable_float_to_int:
            connect_float_to_int(output_file)



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

    output_file.write("\n  //////////////////////////////////////////////////////////////////////////////\n")
    output_file.write("  // CPU IMPLEMENTAION OF C PROCESS                                             \n")
    output_file.write("  //                                                                            \n")
    output_file.write("  // This section of the file contains a CPU implementing the C process.        \n")

    output_file.write("  \n  always @(posedge clk)\n")
    output_file.write("  begin\n\n")

    if memory_size:
        output_file.write("    //implement memory for 4 byte x n arrays\n")
        output_file.write("    if (memory_enable == 1'b1) begin\n")
        output_file.write("      memory[address] <= data_in;\n")
        output_file.write("    end\n")
        output_file.write("    data_out <= memory[address];\n")
        output_file.write("    memory_enable <= 1'b0;\n\n")

    output_file.write("    write_enable_2 <= 0;\n")

    if enable_divider:
        output_file.write("    divider_go <= 0;\n")
    if enable_multiplier:
        output_file.write("    multiplier_go <= 0;\n")
    if enable_adder:
        output_file.write("    adder_go <= 0;\n")
    if enable_long_divider:
        output_file.write("    long_divider_go <= 0;\n")
    if enable_long_multiplier:
        output_file.write("    long_multiplier_go <= 0;\n")
    if enable_long_adder:
        output_file.write("    long_adder_go <= 0;\n")
    if enable_int_to_float:
        output_file.write("    int_to_float_go <= 0;\n")
    if enable_float_to_int:
        output_file.write("    float_to_int_go <= 0;\n")
    if enable_long_to_double:
        output_file.write("    long_to_double_go <= 0;\n")
    if enable_double_to_long:
        output_file.write("    double_to_long_go <= 0;\n")
    if enable_float_to_double:
        output_file.write("    float_to_double_go <= 0;\n")
    if enable_double_to_float:
        output_file.write("    double_to_float_go <= 0;\n")

    output_file.write("    //stage 0 instruction fetch\n")
    output_file.write("    if (stage_0_enable) begin\n")
    output_file.write("      stage_1_enable <= 1;\n")
    output_file.write("      instruction_0 <= instructions[program_counter];\n")
    output_file.write("      opcode_0 = instruction_0[%s:%s];\n"%(
        register_bits * 2 + opcode_bits + 31,
        register_bits * 2 + 32))
    output_file.write("      dest_0 = instruction_0[%s:%s];\n"%(
        register_bits * 2 + 31,
        register_bits + 32))
    output_file.write("      src_0 = instruction_0[%s:32];\n"%(
        register_bits + 31))
    output_file.write("      srcb_0 = instruction_0[%s:0];\n"%(register_bits-1))
    output_file.write("      literal_0 = instruction_0[31:0];\n")
    output_file.write("      if(write_enable_2) begin\n")
    output_file.write("            registers[dest_2] <= result_2;\n")
    output_file.write("      end\n")
    output_file.write("      program_counter_0 <= program_counter;\n")
    output_file.write("      program_counter <= program_counter + 1;\n")
    output_file.write("    end\n\n")

    output_file.write("    //stage 1 opcode fetch\n")
    output_file.write("    if (stage_1_enable) begin\n")
    output_file.write("      stage_2_enable <= 1;\n")
    output_file.write("      register_1 <= registers[src_0];\n")
    output_file.write("      registerb_1 <= registers[srcb_0];\n")
    output_file.write("      dest_1 <= dest_0;\n")
    output_file.write("      literal_1 <= literal_0;\n")
    output_file.write("      opcode_1 <= opcode_0;\n")
    output_file.write("      program_counter_1 <= program_counter_0;\n")
    output_file.write("    end\n\n")

    output_file.write("    //stage 2 opcode fetch\n")
    output_file.write("    if (stage_2_enable) begin\n")
    output_file.write("      dest_2 <= dest_1;\n")
    output_file.write("      case(opcode_1)\n\n")

    #A frame is executed in each state
    for opcode, instruction in enumerate(instruction_set):

        output_file.write("        //%s\n"%(instruction["op"]))
        output_file.write("        16'd%s:\n"%(opcode))
        output_file.write("        begin\n")

        if instruction["op"] == "nop":
            pass

        elif instruction["op"] == "literal":
            output_file.write("          result_2 <= literal_1;\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "move":
            output_file.write("          result_2 <= register_1;\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "not":
            output_file.write("          result_2 <= ~register_1;\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "int_to_float":
            output_file.write("          int_to <= register_1;\n")
            output_file.write("          int_to_float_go <= 1;\n")
            output_file.write("          stage_0_enable <= 0;\n")
            output_file.write("          stage_1_enable <= 0;\n")
            output_file.write("          stage_2_enable <= 0;\n")

        elif instruction["op"] == "float_to_int":
            output_file.write("          float_to <= register_1;\n")
            output_file.write("          float_to_int_go <= 1;\n")
            output_file.write("          stage_0_enable <= 0;\n")
            output_file.write("          stage_1_enable <= 0;\n")
            output_file.write("          stage_2_enable <= 0;\n")

        elif instruction["op"] == "long_to_double":
            output_file.write("          long_to <= {register_hi, register_1};\n")
            output_file.write("          long_to_double_go <= 1;\n")
            output_file.write("          stage_0_enable <= 0;\n")
            output_file.write("          stage_1_enable <= 0;\n")
            output_file.write("          stage_2_enable <= 0;\n")

        elif instruction["op"] == "double_to_long":
            output_file.write("          double_to <= {register_hi, register_1};\n")
            output_file.write("          double_to_long_go <= 1;\n")
            output_file.write("          stage_0_enable <= 0;\n")
            output_file.write("          stage_1_enable <= 0;\n")
            output_file.write("          stage_2_enable <= 0;\n")

        elif instruction["op"] == "float_to_double":
            output_file.write("          float_to_d <= {register_hi, register_1};\n")
            output_file.write("          float_to_double_go <= 1;\n")
            output_file.write("          stage_0_enable <= 0;\n")
            output_file.write("          stage_1_enable <= 0;\n")
            output_file.write("          stage_2_enable <= 0;\n")

        elif instruction["op"] == "double_to_float":
            output_file.write("          double_to_f <= {register_hi, register_1};\n")
            output_file.write("          double_to_float_go <= 1;\n")
            output_file.write("          stage_0_enable <= 0;\n")
            output_file.write("          stage_1_enable <= 0;\n")
            output_file.write("          stage_2_enable <= 0;\n")

        elif instruction["op"] == "load_hi":
            output_file.write("          register_hi <= register_1;\n")
            output_file.write("          registerb_hi <= registerb_1;\n")

        elif instruction["op"] == "add":
            output_file.write("          long_result = register_1 + registerb_1;\n")
            output_file.write("          result_2 <= long_result[31:0];\n")
            output_file.write("          carry <= long_result[32];\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "add_with_carry":
            output_file.write("          long_result = register_1 + registerb_1 + carry;\n")
            output_file.write("          result_2 <= long_result[31:0];\n")
            output_file.write("          carry <= long_result[32];\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "subtract":
            output_file.write("          long_result = register_1 + (~registerb_1) + 1;\n")
            output_file.write("          result_2 <= long_result[31:0];\n")
            output_file.write("          carry <= ~long_result[32];\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "subtract_with_carry":
            output_file.write("          long_result = register_1 + (~registerb_1) + carry;\n")
            output_file.write("          result_2 <= long_result[31:0];\n")
            output_file.write("          carry <= ~long_result[32];\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "multiply":
            output_file.write("          long_result = register_1 * registerb_1;\n")
            output_file.write("          result_2 <= long_result[31:0];\n")
            output_file.write("          result_hi <= long_result[63:32];\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "result_hi":
            output_file.write("          result_2 <= result_hi;\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "or":
            output_file.write("          result_2 <= register_1 | registerb_1;\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "and":
            output_file.write("          result_2 <= register_1 & registerb_1;\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "xor":
            output_file.write("          result_2 <= register_1 ^ registerb_1;\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "shift_left":
            output_file.write("          result_2 <= {register_1[30:0], 1'd0};\n")
            output_file.write("          carry <= register_1[31];\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "shift_left_with_carry":
            output_file.write("          result_2 <= {register_1[30:0], carry};\n")
            output_file.write("          carry <= register_1[31];\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "shift_right":
            output_file.write("          result_2 <= {register_1[31], register_1[31:1]};\n")
            output_file.write("          carry <= register_1[0];\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "unsigned_shift_right":
            output_file.write("          result_2 <= {1'd0, register_1[31:1]};\n")
            output_file.write("          carry <= register_1[0];\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "shift_right_with_carry":
            output_file.write("          result_2 = {carry, register_1[31:1]};\n")
            output_file.write("          carry <= register_1[0];\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "greater":
            output_file.write("          result_2 <= $signed(register_1) > $signed(registerb_1);\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "greater_equal":
            output_file.write("          result_2 <= $signed(register_1) >= $signed(registerb_1);\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "unsigned_greater":
            output_file.write("          result_2 <= $unsigned(register_1) > $unsigned(registerb_1);\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "unsigned_greater_equal":
            output_file.write("          result_2 <= $unsigned(register_1) >= $unsigned(registerb_1);\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "equal":
            output_file.write("          result_2 <= register_1 == registerb_1;\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "not_equal":
            output_file.write("          result_2 <= register_1 != registerb_1;\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "float_add":
            output_file.write("          adder_a <= register_1;\n")
            output_file.write("          adder_b <= registerb_1;\n")
            output_file.write("          adder_go <= 1;\n")
            output_file.write("          stage_0_enable <= 0;\n")
            output_file.write("          stage_1_enable <= 0;\n")
            output_file.write("          stage_2_enable <= 0;\n")

        elif instruction["op"] == "float_subtract":
            output_file.write("          adder_a <= register_1;\n")
            output_file.write("          adder_b <= {~registerb_1[31], registerb_1[30:0]};\n")
            output_file.write("          adder_go <= 1;\n")
            output_file.write("          stage_0_enable <= 0;\n")
            output_file.write("          stage_1_enable <= 0;\n")
            output_file.write("          stage_2_enable <= 0;\n")

        elif instruction["op"] == "float_multiply":
            output_file.write("          multiplier_a <= register_1;\n")
            output_file.write("          multiplier_b <= registerb_1;\n")
            output_file.write("          multiplier_go <= 1;\n")
            output_file.write("          stage_0_enable <= 0;\n")
            output_file.write("          stage_1_enable <= 0;\n")
            output_file.write("          stage_2_enable <= 0;\n")

        elif instruction["op"] == "float_divide":
            output_file.write("          divider_a <= register_1;\n")
            output_file.write("          divider_b <= registerb_1;\n")
            output_file.write("          divider_go <= 1;\n")
            output_file.write("          stage_0_enable <= 0;\n")
            output_file.write("          stage_1_enable <= 0;\n")
            output_file.write("          stage_2_enable <= 0;\n")

        elif instruction["op"] == "long_float_add":
            output_file.write("          long_adder_a <= {register_hi, register_1};\n")
            output_file.write("          long_adder_b <= {registerb_hi, registerb_1};\n")
            output_file.write("          long_adder_go <= 1;\n")
            output_file.write("          stage_0_enable <= 0;\n")
            output_file.write("          stage_1_enable <= 0;\n")
            output_file.write("          stage_2_enable <= 0;\n")

        elif instruction["op"] == "long_float_subtract":
            output_file.write("          long_adder_a <= {register_hi, register_1};\n")
            output_file.write("          long_adder_b <= {~registerb_hi[31], registerb_hi[30:0], registerb_1};\n")
            output_file.write("          long_adder_go <= 1;\n")
            output_file.write("          stage_0_enable <= 0;\n")
            output_file.write("          stage_1_enable <= 0;\n")
            output_file.write("          stage_2_enable <= 0;\n")

        elif instruction["op"] == "long_float_multiply":
            output_file.write("          long_multiplier_a <= {register_hi, register_1};\n")
            output_file.write("          long_multiplier_b <= {registerb_hi, registerb_1};\n")
            output_file.write("          long_multiplier_go <= 1;\n")
            output_file.write("          stage_0_enable <= 0;\n")
            output_file.write("          stage_1_enable <= 0;\n")
            output_file.write("          stage_2_enable <= 0;\n")

        elif instruction["op"] == "long_float_divide":
            output_file.write("          long_divider_a <= {register_hi, register_1};\n")
            output_file.write("          long_divider_b <= {registerb_hi, registerb_1};\n")
            output_file.write("          long_divider_go <= 1;\n")
            output_file.write("          stage_0_enable <= 0;\n")
            output_file.write("          stage_1_enable <= 0;\n")
            output_file.write("          stage_2_enable <= 0;\n")

        elif instruction["op"] == "jmp_if_false":
            output_file.write("          if (register_1 == 0) begin\n");
            output_file.write("            program_counter <= literal_1;\n")
            output_file.write("            stage_0_enable <= 1;\n")
            output_file.write("            stage_1_enable <= 0;\n")
            output_file.write("            stage_2_enable <= 0;\n")
            output_file.write("          end\n")

        elif instruction["op"] == "jmp_if_true":
            output_file.write("          if (register_1 != 0) begin\n");
            output_file.write("            program_counter <= literal_1;\n")
            output_file.write("            stage_0_enable <= 1;\n")
            output_file.write("            stage_1_enable <= 0;\n")
            output_file.write("            stage_2_enable <= 0;\n")
            output_file.write("          end\n")

        elif instruction["op"] == "jmp_and_link":
            output_file.write("          program_counter <= literal_1;\n")
            output_file.write("          result_2 <= program_counter_1 + 1;\n")
            output_file.write("          write_enable_2 <= 1;\n")
            output_file.write("          stage_0_enable <= 1;\n")
            output_file.write("          stage_1_enable <= 0;\n")
            output_file.write("          stage_2_enable <= 0;\n")

        elif instruction["op"] == "jmp_to_reg":
            output_file.write("          program_counter <= register_1;\n")
            output_file.write("          stage_0_enable <= 1;\n")
            output_file.write("          stage_1_enable <= 0;\n")
            output_file.write("          stage_2_enable <= 0;\n")

        elif instruction["op"] == "goto":
            output_file.write("          program_counter <= literal_1;\n")
            output_file.write("          stage_0_enable <= 1;\n")
            output_file.write("          stage_1_enable <= 0;\n")
            output_file.write("          stage_2_enable <= 0;\n")

        elif instruction["op"] == "file_read":
            output_file.write("        16'd%s:\n"%(opcode))
            output_file.write("        begin\n")
            output_file.write("          file_count = $fscanf(%s, \"%%d\\n\", result_2);\n"%(
              input_files[instruction["file_name"]]))
            output_file.write("          write_enable_2 <= 1;\n")
            output_file.write("        end\n\n")

        elif instruction["op"] == "float_file_write":
                output_file.write('          fp_value = (register_1[31]?-1.0:1.0) *\n')
                output_file.write('              (2.0 ** (register_1[30:23]-127.0)) *\n')
                output_file.write('              ({1\'d1, register_1[22:0]} / (2.0**23));\n')
                output_file.write('          $fdisplay (%s, "%%f", fp_value);\n'%(
                  output_files[instruction["file_name"]]))

        elif instruction["op"] == "unsigned_file_write":
                output_file.write("          $fdisplay (%s, \"%%d\", $unsigned(register_1));\n"%(
                  output_files[instruction["file_name"]]))

        elif instruction["op"] == "file_write":
                output_file.write("          $fdisplay (%s, \"%%d\", $signed(register_1));\n"%(
                  output_files[instruction["file_name"]]))

        elif instruction["op"] == "read":
            output_file.write("          stage_0_enable <= 0;\n")
            output_file.write("          stage_1_enable <= 0;\n")
            output_file.write("          stage_2_enable <= 0;\n")
            output_file.write("          case(register_1)\n\n")
            for handle, input_name in allocator.input_names.iteritems():
                output_file.write("            %s:\n"%(handle))
                output_file.write("            begin\n")
                output_file.write("              s_input_%s_ack <= 1'b1;\n"%input_name)
                output_file.write("            end\n")
            output_file.write("          endcase\n")

        elif instruction["op"] == "ready":
            output_file.write("          result_2 <= 0;\n")
            output_file.write("          case(register_1)\n\n")
            for handle, input_name in allocator.input_names.iteritems():
                output_file.write("            %s:\n"%(handle))
                output_file.write("            begin\n")
                output_file.write("              result_2[0] <= s_input_%s_ack;\n"%input_name)
                output_file.write("            end\n")
            output_file.write("          endcase\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "write":
            output_file.write("          stage_0_enable <= 0;\n")
            output_file.write("          stage_1_enable <= 0;\n")
            output_file.write("          stage_2_enable <= 0;\n")
            output_file.write("          case(register_1)\n\n")
            for handle, output_name in allocator.output_names.iteritems():
                output_file.write("            %s:\n"%(handle))
                output_file.write("            begin\n")
                output_file.write("              s_output_%s_stb <= 1'b1;\n"%output_name)
                output_file.write("            end\n")
            output_file.write("          endcase\n")

        elif instruction["op"] == "memory_read_request":
            output_file.write("          address <= register_1;\n")

        elif instruction["op"] == "memory_read_wait":
            pass

        elif instruction["op"] == "memory_read":
            output_file.write("          result_2 <= data_out;\n")
            output_file.write("          write_enable_2 <= 1;\n")

        elif instruction["op"] == "memory_write":
            output_file.write("          address <= register_1;\n")
            output_file.write("          data_in <= registerb_1;\n")
            output_file.write("          memory_enable <= 1'b1;\n")

        elif instruction["op"] == "assert":
            output_file.write("          if (register_1 == 0) begin\n")
            output_file.write("            $display(\"Assertion failed at line: %s in file: %s\");\n"%(
              instruction["line"],
              instruction["file"]))
            output_file.write("            $finish_and_return(1);\n")
            output_file.write("          end\n")

        elif instruction["op"] == "wait_clocks":
            output_file.write("          timer <= register_1;\n")
            output_file.write("          timer_enable <= 1;\n")
            output_file.write("          stage_0_enable <= 0;\n")
            output_file.write("          stage_1_enable <= 0;\n")
            output_file.write("          stage_2_enable <= 0;\n")

        elif instruction["op"] == "report":
            output_file.write('          $display ("%%d (report at line: %s in file: %s)", $signed(register_1));\n'%(
                instruction["line"],
                instruction["file"],))

        elif instruction["op"] == "long_report":
            output_file.write('          $display ("%%d (report at line: %s in file: %s)", $signed({register_hi, register_1}));\n'%(
                instruction["line"],
                instruction["file"],))

        elif instruction["op"] == "float_report":
           output_file.write('          fp_value = (register_1[31]?-1.0:1.0) *\n')
           output_file.write('              (2.0 ** (register_1[30:23]-127.0)) *\n')
           output_file.write('              ({1\'d1, register_1[22:0]} / (2.0**23));\n')
           output_file.write('          $display ("%%f (report at line: %s in file: %s)", fp_value);\n'%(
                  instruction["line"],
                  instruction["file"]))

        elif instruction["op"] == "long_float_report":
           output_file.write('          fp_value = (register_hi[31]?-1.0:1.0) *\n')
           output_file.write('              (2.0 ** (register_hi[30:20]-1023.0)) *\n')
           output_file.write('              ({1\'d1, register_hi[19:0], register_1} / (2.0**52));\n')
           output_file.write('          $display ("%%f (report at line: %s in file: %s)", fp_value);\n'%(
                  instruction["line"],
                  instruction["file"]))

        elif instruction["op"] == "unsigned_report":
           output_file.write('          $display ("%%d (report at line: %s in file: %s)", $unsigned(register_1));\n'%(
	       instruction["line"],
	       instruction["file"]))

        elif instruction["op"] == "long_unsigned_report":
           output_file.write('          $display ("%%d (report at line: %s in file: %s)", $unsigned({register_hi, register_1}));\n'%(
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
            output_file.write("          stage_0_enable <= 0;\n")
            output_file.write("          stage_1_enable <= 0;\n")
            output_file.write("          stage_2_enable <= 0;\n")

        else:
            print "unsuported instruction", instruction["op"]
            print instruction

        output_file.write("        end\n\n")


    output_file.write("       endcase\n")
    output_file.write("    end\n")

    for input_ in allocator.input_names.values():

        output_file.write("    if (s_input_%s_ack == 1'b1 && input_%s_stb == 1'b1) begin\n"%(
          input_,
          input_))
        output_file.write("       result_2 <= input_%s;\n"%input_)
        output_file.write("       write_enable_2 <= 1;\n")
        output_file.write("       s_input_%s_ack <= 1'b0;\n"%input_)
        output_file.write("       stage_0_enable <= 1;\n")
        output_file.write("       stage_1_enable <= 1;\n")
        output_file.write("       stage_2_enable <= 1;\n")
        output_file.write("     end\n\n")

    for output_ in allocator.output_names.values():

        output_file.write("     if (s_output_%s_stb == 1'b1 && output_%s_ack == 1'b1) begin\n"%(
          output_,
          output_))
        output_file.write("       s_output_%s_stb <= 1'b0;\n"%output_)
        output_file.write("       stage_0_enable <= 1;\n")
        output_file.write("       stage_1_enable <= 1;\n")
        output_file.write("       stage_2_enable <= 1;\n")
        output_file.write("     end\n\n")

    output_file.write("    if (timer == 0) begin\n")
    output_file.write("      if (timer_enable) begin\n")
    output_file.write("         stage_0_enable <= 1;\n")
    output_file.write("         stage_1_enable <= 1;\n")
    output_file.write("         stage_2_enable <= 1;\n")
    output_file.write("         timer_enable <= 0;\n")
    output_file.write("      end\n")
    output_file.write("    end else begin\n")
    output_file.write("      timer <= timer - 1;\n")
    output_file.write("    end\n\n")


    if enable_adder:
        output_file.write("    if (adder_done) begin\n")
        output_file.write("      result_2 <= adder_z;\n")
        output_file.write("      write_enable_2 <= 1;\n")
        output_file.write("      stage_0_enable <= 1;\n")
        output_file.write("      stage_1_enable <= 1;\n")
        output_file.write("      stage_2_enable <= 1;\n")
        output_file.write("    end\n\n")

    if enable_multiplier:
        output_file.write("    if (multiplier_done) begin\n")
        output_file.write("      result_2 <= multiplier_z;\n")
        output_file.write("      write_enable_2 <= 1;\n")
        output_file.write("      stage_0_enable <= 1;\n")
        output_file.write("      stage_1_enable <= 1;\n")
        output_file.write("      stage_2_enable <= 1;\n")
        output_file.write("    end\n\n")

    if enable_divider:
        output_file.write("    if (divider_done) begin\n")
        output_file.write("      result_2 <= divider_z;\n")
        output_file.write("      write_enable_2 <= 1;\n")
        output_file.write("      stage_0_enable <= 1;\n")
        output_file.write("      stage_1_enable <= 1;\n")
        output_file.write("      stage_2_enable <= 1;\n")
        output_file.write("    end\n\n")

    if enable_long_adder:
        output_file.write("    if (long_adder_done) begin\n")
        output_file.write("      result_2 <= long_adder_z[31:0];\n")
        output_file.write("      result_hi <= long_adder_z[63:32];\n")
        output_file.write("      write_enable_2 <= 1;\n")
        output_file.write("      stage_0_enable <= 1;\n")
        output_file.write("      stage_1_enable <= 1;\n")
        output_file.write("      stage_2_enable <= 1;\n")
        output_file.write("    end\n\n")

    if enable_long_multiplier:
        output_file.write("    if (long_multiplier_done) begin\n")
        output_file.write("      result_2 <= long_multiplier_z[31:0];\n")
        output_file.write("      result_hi <= long_multiplier_z[63:32];\n")
        output_file.write("      write_enable_2 <= 1;\n")
        output_file.write("      stage_0_enable <= 1;\n")
        output_file.write("      stage_1_enable <= 1;\n")
        output_file.write("      stage_2_enable <= 1;\n")
        output_file.write("    end\n\n")

    if enable_long_divider:
        output_file.write("    if (long_divider_done) begin\n")
        output_file.write("      result_2 <= long_divider_z[31:0];\n")
        output_file.write("      result_hi <= long_divider_z[63:32];\n")
        output_file.write("      write_enable_2 <= 1;\n")
        output_file.write("      stage_0_enable <= 1;\n")
        output_file.write("      stage_1_enable <= 1;\n")
        output_file.write("      stage_2_enable <= 1;\n")
        output_file.write("    end\n\n")

    if enable_int_to_float:
        output_file.write("    if (int_to_float_done) begin\n")
        output_file.write("      result_2 <= to_float;\n")
        output_file.write("      write_enable_2 <= 1;\n")
        output_file.write("      stage_0_enable <= 1;\n")
        output_file.write("      stage_1_enable <= 1;\n")
        output_file.write("      stage_2_enable <= 1;\n")
        output_file.write("    end\n\n")

    if enable_float_to_int:
        output_file.write("    if (float_to_int_done) begin\n")
        output_file.write("      result_2 <= to_int;\n")
        output_file.write("      write_enable_2 <= 1;\n")
        output_file.write("      stage_0_enable <= 1;\n")
        output_file.write("      stage_1_enable <= 1;\n")
        output_file.write("      stage_2_enable <= 1;\n")
        output_file.write("    end\n\n")

    if enable_long_to_double:
        output_file.write("    if (long_to_double_done) begin\n")
        output_file.write("      result_2 <= to_double[31:0];\n")
        output_file.write("      result_hi <= to_double[63:32];\n")
        output_file.write("      write_enable_2 <= 1;\n")
        output_file.write("      stage_0_enable <= 1;\n")
        output_file.write("      stage_1_enable <= 1;\n")
        output_file.write("      stage_2_enable <= 1;\n")
        output_file.write("    end\n\n")

    if enable_double_to_long:
        output_file.write("    if (double_to_long_done) begin\n")
        output_file.write("      result_2 <= to_long[31:0];\n")
        output_file.write("      result_hi <= to_long[63:32];\n")
        output_file.write("      write_enable_2 <= 1;\n")
        output_file.write("      stage_0_enable <= 1;\n")
        output_file.write("      stage_1_enable <= 1;\n")
        output_file.write("      stage_2_enable <= 1;\n")
        output_file.write("    end\n\n")

    if enable_float_to_double:
        output_file.write("    if (float_to_double_done) begin\n")
        output_file.write("      result_2 <= f_to_double[31:0];\n")
        output_file.write("      result_hi <= f_to_double[63:32];\n")
        output_file.write("      write_enable_2 <= 1;\n")
        output_file.write("      stage_0_enable <= 1;\n")
        output_file.write("      stage_1_enable <= 1;\n")
        output_file.write("      stage_2_enable <= 1;\n")
        output_file.write("    end\n\n")

    if enable_double_to_float:
        output_file.write("    if (double_to_float_done) begin\n")
        output_file.write("      result_2 <= d_to_float[31:0];\n")
        output_file.write("      result_hi <= d_to_float[63:32];\n")
        output_file.write("      write_enable_2 <= 1;\n")
        output_file.write("      stage_0_enable <= 1;\n")
        output_file.write("      stage_1_enable <= 1;\n")
        output_file.write("      stage_2_enable <= 1;\n")
        output_file.write("    end\n\n")

    #Reset program counter and control signals
    output_file.write("    if (rst == 1'b1) begin\n")
    output_file.write("      stage_0_enable <= 1;\n")
    output_file.write("      stage_1_enable <= 0;\n")
    output_file.write("      stage_2_enable <= 0;\n")
    output_file.write("      timer <= 0;\n")
    output_file.write("      timer_enable <= 0;\n")
    output_file.write("      program_counter <= 0;\n")
    for i in inputs:
        output_file.write("      s_input_%s_ack <= 0;\n"%(i))
    for i in outputs:
        output_file.write("      s_output_%s_stb <= 0;\n"%(i))
    output_file.write("    end\n")
    output_file.write("  end\n")
    for i in inputs:
        output_file.write("  assign input_%s_ack = s_input_%s_ack;\n"%(i, i))
    for i in outputs:
        output_file.write("  assign output_%s_stb = s_output_%s_stb;\n"%(i, i))
        output_file.write("  assign output_%s = s_output_%s;\n"%(i, i))
    output_file.write("\nendmodule\n")

    return inputs, outputs

def connect_float_to_int(output_file):
    output_file.write("  \n  float_to_int float_to_int_1(\n")
    output_file.write("    .clk(clk),\n")
    output_file.write("    .rst(rst),\n")
    output_file.write("    .input_a(float_to),\n")
    output_file.write("    .input_a_stb(float_to_stb),\n")
    output_file.write("    .input_a_ack(float_to_ack),\n")
    output_file.write("    .output_z(to_int),\n")
    output_file.write("    .output_z_stb(to_int_stb),\n")
    output_file.write("    .output_z_ack(to_int_ack)\n")
    output_file.write("  );\n\n")
    output_file.write("  \n  always @(posedge clk)\n")
    output_file.write("  begin\n\n")
    output_file.write("    float_to_int_done <= 0;\n")
    output_file.write("    case(float_to_int_state)\n\n")
    output_file.write("      wait_go:\n")
    output_file.write("      begin\n")
    output_file.write("        if (float_to_int_go) begin\n")
    output_file.write("          float_to_int_state <= write_a;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      write_a:\n")
    output_file.write("      begin\n")
    output_file.write("        float_to_stb <= 1;\n")
    output_file.write("        if (float_to_stb && float_to_ack) begin\n")
    output_file.write("          float_to_stb <= 0;\n")
    output_file.write("          float_to_int_state <= read_z;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      read_z:\n")
    output_file.write("      begin\n")
    output_file.write("        to_int_ack <= 1;\n")
    output_file.write("        if (to_int_stb && to_int_ack) begin\n")
    output_file.write("          to_int_ack <= 0;\n")
    output_file.write("          float_to_int_state <= wait_go;\n")
    output_file.write("          float_to_int_done <= 1;\n")
    output_file.write("        end\n")
    output_file.write("      end\n")
    output_file.write("    endcase\n")
    output_file.write("    if (rst) begin\n")
    output_file.write("      float_to_int_state <= wait_go;\n")
    output_file.write("      float_to_stb <= 0;\n")
    output_file.write("      to_int_ack <= 0;\n")
    output_file.write("    end\n")
    output_file.write("  end\n\n")

def connect_int_to_float(output_file):
    output_file.write("  \n  int_to_float int_to_float_1(\n")
    output_file.write("    .clk(clk),\n")
    output_file.write("    .rst(rst),\n")
    output_file.write("    .input_a(int_to),\n")
    output_file.write("    .input_a_stb(int_to_stb),\n")
    output_file.write("    .input_a_ack(int_to_ack),\n")
    output_file.write("    .output_z(to_float),\n")
    output_file.write("    .output_z_stb(to_float_stb),\n")
    output_file.write("    .output_z_ack(to_float_ack)\n")
    output_file.write("  );\n\n")
    output_file.write("  \n  always @(posedge clk)\n")
    output_file.write("  begin\n\n")
    output_file.write("    int_to_float_done <= 0;\n")
    output_file.write("    case(int_to_float_state)\n\n")
    output_file.write("      wait_go:\n")
    output_file.write("      begin\n")
    output_file.write("        if (int_to_float_go) begin\n")
    output_file.write("          int_to_float_state <= write_a;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      write_a:\n")
    output_file.write("      begin\n")
    output_file.write("        int_to_stb <= 1;\n")
    output_file.write("        if (int_to_stb && int_to_ack) begin\n")
    output_file.write("          int_to_stb <= 0;\n")
    output_file.write("          int_to_float_state <= read_z;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      read_z:\n")
    output_file.write("      begin\n")
    output_file.write("        to_float_ack <= 1;\n")
    output_file.write("        if (to_float_stb && to_float_ack) begin\n")
    output_file.write("          to_float_ack <= 0;\n")
    output_file.write("          int_to_float_state <= wait_go;\n")
    output_file.write("          int_to_float_done <= 1;\n")
    output_file.write("        end\n")
    output_file.write("      end\n")
    output_file.write("    endcase\n")
    output_file.write("    if (rst) begin\n")
    output_file.write("      int_to_float_state <= wait_go;\n")
    output_file.write("      int_to_stb <= 0;\n")
    output_file.write("      to_float_ack <= 0;\n")
    output_file.write("    end\n")
    output_file.write("  end\n\n")

def connect_double_to_long(output_file):
    output_file.write("  \n  double_to_int double_to_long_1(\n")
    output_file.write("    .clk(clk),\n")
    output_file.write("    .rst(rst),\n")
    output_file.write("    .input_a(double_to),\n")
    output_file.write("    .input_a_stb(double_to_stb),\n")
    output_file.write("    .input_a_ack(double_to_ack),\n")
    output_file.write("    .output_z(to_long),\n")
    output_file.write("    .output_z_stb(to_long_stb),\n")
    output_file.write("    .output_z_ack(to_long_ack)\n")
    output_file.write("  );\n\n")
    output_file.write("  \n  always @(posedge clk)\n")
    output_file.write("  begin\n\n")
    output_file.write("    double_to_long_done <= 0;\n")
    output_file.write("    case(double_to_long_state)\n\n")
    output_file.write("      wait_go:\n")
    output_file.write("      begin\n")
    output_file.write("        if (double_to_long_go) begin\n")
    output_file.write("          double_to_long_state <= write_a;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      write_a:\n")
    output_file.write("      begin\n")
    output_file.write("        double_to_stb <= 1;\n")
    output_file.write("        if (double_to_stb && double_to_ack) begin\n")
    output_file.write("          double_to_stb <= 0;\n")
    output_file.write("          double_to_long_state <= read_z;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      read_z:\n")
    output_file.write("      begin\n")
    output_file.write("        to_long_ack <= 1;\n")
    output_file.write("        if (to_long_stb && to_long_ack) begin\n")
    output_file.write("          to_long_ack <= 0;\n")
    output_file.write("          double_to_long_state <= wait_go;\n")
    output_file.write("          double_to_long_done <= 1;\n")
    output_file.write("        end\n")
    output_file.write("      end\n")
    output_file.write("    endcase\n")
    output_file.write("    if (rst) begin\n")
    output_file.write("      double_to_long_state <= wait_go;\n")
    output_file.write("      double_to_stb <= 0;\n")
    output_file.write("      to_long_ack <= 0;\n")
    output_file.write("    end\n")
    output_file.write("  end\n\n")

def connect_long_to_double(output_file):
    output_file.write("  \n  int_to_double long_to_double_1(\n")
    output_file.write("    .clk(clk),\n")
    output_file.write("    .rst(rst),\n")
    output_file.write("    .input_a(long_to),\n")
    output_file.write("    .input_a_stb(long_to_stb),\n")
    output_file.write("    .input_a_ack(long_to_ack),\n")
    output_file.write("    .output_z(to_double),\n")
    output_file.write("    .output_z_stb(to_double_stb),\n")
    output_file.write("    .output_z_ack(to_double_ack)\n")
    output_file.write("  );\n\n")
    output_file.write("  \n  always @(posedge clk)\n")
    output_file.write("  begin\n\n")
    output_file.write("    long_to_double_done <= 0;\n")
    output_file.write("    case(long_to_double_state)\n\n")
    output_file.write("      wait_go:\n")
    output_file.write("      begin\n")
    output_file.write("        if (long_to_double_go) begin\n")
    output_file.write("          long_to_double_state <= write_a;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      write_a:\n")
    output_file.write("      begin\n")
    output_file.write("        long_to_stb <= 1;\n")
    output_file.write("        if (long_to_stb && long_to_ack) begin\n")
    output_file.write("          long_to_stb <= 0;\n")
    output_file.write("          long_to_double_state <= read_z;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      read_z:\n")
    output_file.write("      begin\n")
    output_file.write("        to_double_ack <= 1;\n")
    output_file.write("        if (to_double_stb && to_double_ack) begin\n")
    output_file.write("          to_double_ack <= 0;\n")
    output_file.write("          long_to_double_state <= wait_go;\n")
    output_file.write("          long_to_double_done <= 1;\n")
    output_file.write("        end\n")
    output_file.write("      end\n")
    output_file.write("    endcase\n")
    output_file.write("    if (rst) begin\n")
    output_file.write("      long_to_double_state <= wait_go;\n")
    output_file.write("      long_to_stb <= 0;\n")
    output_file.write("      to_double_ack <= 0;\n")
    output_file.write("    end\n")
    output_file.write("  end\n\n")

def connect_double_to_float(output_file):
    output_file.write("  \n  double_to_float double_to_float_1(\n")
    output_file.write("    .clk(clk),\n")
    output_file.write("    .rst(rst),\n")
    output_file.write("    .input_a(double_to_f),\n")
    output_file.write("    .input_a_stb(double_to_f_stb),\n")
    output_file.write("    .input_a_ack(double_to_f_ack),\n")
    output_file.write("    .output_z(d_to_float),\n")
    output_file.write("    .output_z_stb(d_to_float_stb),\n")
    output_file.write("    .output_z_ack(d_to_float_ack)\n")
    output_file.write("  );\n\n")
    output_file.write("  \n  always @(posedge clk)\n")
    output_file.write("  begin\n\n")
    output_file.write("    double_to_float_done <= 0;\n")
    output_file.write("    case(double_to_float_state)\n\n")
    output_file.write("      wait_go:\n")
    output_file.write("      begin\n")
    output_file.write("        if (double_to_float_go) begin\n")
    output_file.write("          double_to_float_state <= write_a;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      write_a:\n")
    output_file.write("      begin\n")
    output_file.write("        double_to_f_stb <= 1;\n")
    output_file.write("        if (double_to_f_stb && double_to_f_ack) begin\n")
    output_file.write("          double_to_f_stb <= 0;\n")
    output_file.write("          double_to_float_state <= read_z;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      read_z:\n")
    output_file.write("      begin\n")
    output_file.write("        d_to_float_ack <= 1;\n")
    output_file.write("        if (d_to_float_stb && d_to_float_ack) begin\n")
    output_file.write("          d_to_float_ack <= 0;\n")
    output_file.write("          double_to_float_state <= wait_go;\n")
    output_file.write("          double_to_float_done <= 1;\n")
    output_file.write("        end\n")
    output_file.write("      end\n")
    output_file.write("    endcase\n")
    output_file.write("    if (rst) begin\n")
    output_file.write("      double_to_float_state <= wait_go;\n")
    output_file.write("      double_to_f_stb <= 0;\n")
    output_file.write("      d_to_float_ack <= 0;\n")
    output_file.write("    end\n")
    output_file.write("  end\n\n")

def connect_float_to_double(output_file):
    output_file.write("  \n  float_to_double float_to_double_1(\n")
    output_file.write("    .clk(clk),\n")
    output_file.write("    .rst(rst),\n")
    output_file.write("    .input_a(float_to_d),\n")
    output_file.write("    .input_a_stb(float_to_d_stb),\n")
    output_file.write("    .input_a_ack(float_to_d_ack),\n")
    output_file.write("    .output_z(f_to_double),\n")
    output_file.write("    .output_z_stb(f_to_double_stb),\n")
    output_file.write("    .output_z_ack(f_to_double_ack)\n")
    output_file.write("  );\n\n")
    output_file.write("  \n  always @(posedge clk)\n")
    output_file.write("  begin\n\n")
    output_file.write("    float_to_double_done <= 0;\n")
    output_file.write("    case(float_to_double_state)\n\n")
    output_file.write("      wait_go:\n")
    output_file.write("      begin\n")
    output_file.write("        if (float_to_double_go) begin\n")
    output_file.write("          float_to_double_state <= write_a;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      write_a:\n")
    output_file.write("      begin\n")
    output_file.write("        float_to_d_stb <= 1;\n")
    output_file.write("        if (float_to_d_stb && float_to_d_ack) begin\n")
    output_file.write("          float_to_d_stb <= 0;\n")
    output_file.write("          float_to_double_state <= read_z;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      read_z:\n")
    output_file.write("      begin\n")
    output_file.write("        f_to_double_ack <= 1;\n")
    output_file.write("        if (f_to_double_stb && f_to_double_ack) begin\n")
    output_file.write("          f_to_double_ack <= 0;\n")
    output_file.write("          float_to_double_state <= wait_go;\n")
    output_file.write("          float_to_double_done <= 1;\n")
    output_file.write("        end\n")
    output_file.write("      end\n")
    output_file.write("    endcase\n")
    output_file.write("    if (rst) begin\n")
    output_file.write("      float_to_double_state <= wait_go;\n")
    output_file.write("      float_to_d_stb <= 0;\n")
    output_file.write("      f_to_double_ack <= 0;\n")
    output_file.write("    end\n")
    output_file.write("  end\n\n")

def connect_divider(output_file):
    output_file.write("  \n  divider divider_1(\n")
    output_file.write("    .clk(clk),\n")
    output_file.write("    .rst(rst),\n")
    output_file.write("    .input_a(divider_a),\n")
    output_file.write("    .input_a_stb(divider_a_stb),\n")
    output_file.write("    .input_a_ack(divider_a_ack),\n")
    output_file.write("    .input_b(divider_b),\n")
    output_file.write("    .input_b_stb(divider_b_stb),\n")
    output_file.write("    .input_b_ack(divider_b_ack),\n")
    output_file.write("    .output_z(divider_z),\n")
    output_file.write("    .output_z_stb(divider_z_stb),\n")
    output_file.write("    .output_z_ack(divider_z_ack)\n")
    output_file.write("  );\n\n")
    output_file.write("  \n  always @(posedge clk)\n")
    output_file.write("  begin\n\n")
    output_file.write("    divider_done <= 0;\n")
    output_file.write("    case(div_state)\n\n")
    output_file.write("      wait_go:\n")
    output_file.write("      begin\n")
    output_file.write("        if (divider_go) begin\n")
    output_file.write("          div_state <= write_a;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      write_a:\n")
    output_file.write("      begin\n")
    output_file.write("        divider_a_stb <= 1;\n")
    output_file.write("        if (divider_a_stb && divider_a_ack) begin\n")
    output_file.write("          divider_a_stb <= 0;\n")
    output_file.write("          div_state <= write_b;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      write_b:\n")
    output_file.write("      begin\n")
    output_file.write("        divider_b_stb <= 1;\n")
    output_file.write("        if (divider_b_stb && divider_b_ack) begin\n")
    output_file.write("          divider_b_stb <= 0;\n")
    output_file.write("          div_state <= read_z;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      read_z:\n")
    output_file.write("      begin\n")
    output_file.write("        divider_z_ack <= 1;\n")
    output_file.write("        if (divider_z_stb && divider_z_ack) begin\n")
    output_file.write("          divider_z_ack <= 0;\n")
    output_file.write("          div_state <= wait_go;\n")
    output_file.write("          divider_done <= 1;\n")
    output_file.write("        end\n")
    output_file.write("      end\n")
    output_file.write("    endcase\n")
    output_file.write("    if (rst) begin\n")
    output_file.write("      div_state <= wait_go;\n")
    output_file.write("      divider_a_stb <= 0;\n")
    output_file.write("      divider_b_stb <= 0;\n")
    output_file.write("      divider_z_ack <= 0;\n")
    output_file.write("    end\n")
    output_file.write("  end\n\n")

def connect_multiplier(output_file):
    output_file.write("  \n  multiplier multiplier_1(\n")
    output_file.write("    .clk(clk),\n")
    output_file.write("    .rst(rst),\n")
    output_file.write("    .input_a(multiplier_a),\n")
    output_file.write("    .input_a_stb(multiplier_a_stb),\n")
    output_file.write("    .input_a_ack(multiplier_a_ack),\n")
    output_file.write("    .input_b(multiplier_b),\n")
    output_file.write("    .input_b_stb(multiplier_b_stb),\n")
    output_file.write("    .input_b_ack(multiplier_b_ack),\n")
    output_file.write("    .output_z(multiplier_z),\n")
    output_file.write("    .output_z_stb(multiplier_z_stb),\n")
    output_file.write("    .output_z_ack(multiplier_z_ack)\n")
    output_file.write("  );\n\n")
    output_file.write("  \n  always @(posedge clk)\n")
    output_file.write("  begin\n\n")
    output_file.write("    multiplier_done <= 0;\n")
    output_file.write("    case(mul_state)\n\n")
    output_file.write("      wait_go:\n")
    output_file.write("      begin\n")
    output_file.write("        if (multiplier_go) begin\n")
    output_file.write("          mul_state <= write_a;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      write_a:\n")
    output_file.write("      begin\n")
    output_file.write("        multiplier_a_stb <= 1;\n")
    output_file.write("        if (multiplier_a_stb && multiplier_a_ack) begin\n")
    output_file.write("          multiplier_a_stb <= 0;\n")
    output_file.write("          mul_state <= write_b;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      write_b:\n")
    output_file.write("      begin\n")
    output_file.write("        multiplier_b_stb <= 1;\n")
    output_file.write("        if (multiplier_b_stb && multiplier_b_ack) begin\n")
    output_file.write("          multiplier_b_stb <= 0;\n")
    output_file.write("          mul_state <= read_z;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      read_z:\n")
    output_file.write("      begin\n")
    output_file.write("        multiplier_z_ack <= 1;\n")
    output_file.write("        if (multiplier_z_stb && multiplier_z_ack) begin\n")
    output_file.write("          multiplier_z_ack <= 0;\n")
    output_file.write("          mul_state <= wait_go;\n")
    output_file.write("          multiplier_done <= 1;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("    endcase\n\n")
    output_file.write("    if (rst) begin\n")
    output_file.write("      mul_state <= wait_go;\n")
    output_file.write("      multiplier_a_stb <= 0;\n")
    output_file.write("      multiplier_b_stb <= 0;\n")
    output_file.write("      multiplier_z_ack <= 0;\n")
    output_file.write("    end\n")
    output_file.write("  end\n\n")

def connect_adder(output_file):
    output_file.write("  \n  adder adder_1(\n")
    output_file.write("    .clk(clk),\n")
    output_file.write("    .rst(rst),\n")
    output_file.write("    .input_a(adder_a),\n")
    output_file.write("    .input_a_stb(adder_a_stb),\n")
    output_file.write("    .input_a_ack(adder_a_ack),\n")
    output_file.write("    .input_b(adder_b),\n")
    output_file.write("    .input_b_stb(adder_b_stb),\n")
    output_file.write("    .input_b_ack(adder_b_ack),\n")
    output_file.write("    .output_z(adder_z),\n")
    output_file.write("    .output_z_stb(adder_z_stb),\n")
    output_file.write("    .output_z_ack(adder_z_ack)\n")
    output_file.write("  );\n\n")
    output_file.write("  \n  always @(posedge clk)\n")
    output_file.write("  begin\n\n")
    output_file.write("    adder_done <= 0;\n")
    output_file.write("    case(add_state)\n\n")
    output_file.write("      wait_go:\n")
    output_file.write("      begin\n")
    output_file.write("        if (adder_go) begin\n")
    output_file.write("          add_state <= write_a;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      write_a:\n")
    output_file.write("      begin\n")
    output_file.write("        adder_a_stb <= 1;\n")
    output_file.write("        if (adder_a_stb && adder_a_ack) begin\n")
    output_file.write("          adder_a_stb <= 0;\n")
    output_file.write("          add_state <= write_b;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      write_b:\n")
    output_file.write("      begin\n")
    output_file.write("        adder_b_stb <= 1;\n")
    output_file.write("        if (adder_b_stb && adder_b_ack) begin\n")
    output_file.write("          adder_b_stb <= 0;\n")
    output_file.write("          add_state <= read_z;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      read_z:\n")
    output_file.write("      begin\n")
    output_file.write("        adder_z_ack <= 1;\n")
    output_file.write("        if (adder_z_stb && adder_z_ack) begin\n")
    output_file.write("          adder_z_ack <= 0;\n")
    output_file.write("          add_state <= wait_go;\n")
    output_file.write("          adder_done <= 1;\n")
    output_file.write("        end\n")
    output_file.write("      end\n")
    output_file.write("    endcase\n")
    output_file.write("    if (rst) begin\n")
    output_file.write("      add_state <= wait_go;\n")
    output_file.write("      adder_a_stb <= 0;\n")
    output_file.write("      adder_b_stb <= 0;\n")
    output_file.write("      adder_z_ack <= 0;\n")
    output_file.write("    end\n")
    output_file.write("  end\n\n")

def connect_long_divider(output_file):
    output_file.write("  \n  double_divider long_divider_1(\n")
    output_file.write("    .clk(clk),\n")
    output_file.write("    .rst(rst),\n")
    output_file.write("    .input_a(long_divider_a),\n")
    output_file.write("    .input_a_stb(long_divider_a_stb),\n")
    output_file.write("    .input_a_ack(long_divider_a_ack),\n")
    output_file.write("    .input_b(long_divider_b),\n")
    output_file.write("    .input_b_stb(long_divider_b_stb),\n")
    output_file.write("    .input_b_ack(long_divider_b_ack),\n")
    output_file.write("    .output_z(long_divider_z),\n")
    output_file.write("    .output_z_stb(long_divider_z_stb),\n")
    output_file.write("    .output_z_ack(long_divider_z_ack)\n")
    output_file.write("  );\n\n")
    output_file.write("  \n  always @(posedge clk)\n")
    output_file.write("  begin\n\n")
    output_file.write("    long_divider_done <= 0;\n")
    output_file.write("    case(long_div_state)\n\n")
    output_file.write("      wait_go:\n")
    output_file.write("      begin\n")
    output_file.write("        if (long_divider_go) begin\n")
    output_file.write("          long_div_state <= write_a;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      write_a:\n")
    output_file.write("      begin\n")
    output_file.write("        long_divider_a_stb <= 1;\n")
    output_file.write("        if (long_divider_a_stb && long_divider_a_ack) begin\n")
    output_file.write("          long_divider_a_stb <= 0;\n")
    output_file.write("          long_div_state <= write_b;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      write_b:\n")
    output_file.write("      begin\n")
    output_file.write("        long_divider_b_stb <= 1;\n")
    output_file.write("        if (long_divider_b_stb && long_divider_b_ack) begin\n")
    output_file.write("          long_divider_b_stb <= 0;\n")
    output_file.write("          long_div_state <= read_z;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      read_z:\n")
    output_file.write("      begin\n")
    output_file.write("        long_divider_z_ack <= 1;\n")
    output_file.write("        if (long_divider_z_stb && long_divider_z_ack) begin\n")
    output_file.write("          long_divider_z_ack <= 0;\n")
    output_file.write("          long_div_state <= wait_go;\n")
    output_file.write("          long_divider_done <= 1;\n")
    output_file.write("        end\n")
    output_file.write("      end\n")
    output_file.write("    endcase\n")
    output_file.write("    if (rst) begin\n")
    output_file.write("      long_div_state <= wait_go;\n")
    output_file.write("      long_divider_a_stb <= 0;\n")
    output_file.write("      long_divider_b_stb <= 0;\n")
    output_file.write("      long_divider_z_ack <= 0;\n")
    output_file.write("    end\n")
    output_file.write("  end\n\n")

def connect_long_multiplier(output_file):
    output_file.write("  \n  double_multiplier long_multiplier_1(\n")
    output_file.write("    .clk(clk),\n")
    output_file.write("    .rst(rst),\n")
    output_file.write("    .input_a(long_multiplier_a),\n")
    output_file.write("    .input_a_stb(long_multiplier_a_stb),\n")
    output_file.write("    .input_a_ack(long_multiplier_a_ack),\n")
    output_file.write("    .input_b(long_multiplier_b),\n")
    output_file.write("    .input_b_stb(long_multiplier_b_stb),\n")
    output_file.write("    .input_b_ack(long_multiplier_b_ack),\n")
    output_file.write("    .output_z(long_multiplier_z),\n")
    output_file.write("    .output_z_stb(long_multiplier_z_stb),\n")
    output_file.write("    .output_z_ack(long_multiplier_z_ack)\n")
    output_file.write("  );\n\n")
    output_file.write("  \n  always @(posedge clk)\n")
    output_file.write("  begin\n\n")
    output_file.write("    long_multiplier_done <= 0;\n")
    output_file.write("    case(long_mul_state)\n\n")
    output_file.write("      wait_go:\n")
    output_file.write("      begin\n")
    output_file.write("        if (long_multiplier_go) begin\n")
    output_file.write("          long_mul_state <= write_a;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      write_a:\n")
    output_file.write("      begin\n")
    output_file.write("        long_multiplier_a_stb <= 1;\n")
    output_file.write("        if (long_multiplier_a_stb && long_multiplier_a_ack) begin\n")
    output_file.write("          long_multiplier_a_stb <= 0;\n")
    output_file.write("          long_mul_state <= write_b;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      write_b:\n")
    output_file.write("      begin\n")
    output_file.write("        long_multiplier_b_stb <= 1;\n")
    output_file.write("        if (long_multiplier_b_stb && long_multiplier_b_ack) begin\n")
    output_file.write("          long_multiplier_b_stb <= 0;\n")
    output_file.write("          long_mul_state <= read_z;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      read_z:\n")
    output_file.write("      begin\n")
    output_file.write("        long_multiplier_z_ack <= 1;\n")
    output_file.write("        if (long_multiplier_z_stb && long_multiplier_z_ack) begin\n")
    output_file.write("          long_multiplier_z_ack <= 0;\n")
    output_file.write("          long_mul_state <= wait_go;\n")
    output_file.write("          long_multiplier_done <= 1;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("    endcase\n\n")
    output_file.write("    if (rst) begin\n")
    output_file.write("      long_mul_state <= wait_go;\n")
    output_file.write("      long_multiplier_a_stb <= 0;\n")
    output_file.write("      long_multiplier_b_stb <= 0;\n")
    output_file.write("      long_multiplier_z_ack <= 0;\n")
    output_file.write("    end\n")
    output_file.write("  end\n\n")

def connect_long_adder(output_file):
    output_file.write("  \n  double_adder long_adder_1(\n")
    output_file.write("    .clk(clk),\n")
    output_file.write("    .rst(rst),\n")
    output_file.write("    .input_a(long_adder_a),\n")
    output_file.write("    .input_a_stb(long_adder_a_stb),\n")
    output_file.write("    .input_a_ack(long_adder_a_ack),\n")
    output_file.write("    .input_b(long_adder_b),\n")
    output_file.write("    .input_b_stb(long_adder_b_stb),\n")
    output_file.write("    .input_b_ack(long_adder_b_ack),\n")
    output_file.write("    .output_z(long_adder_z),\n")
    output_file.write("    .output_z_stb(long_adder_z_stb),\n")
    output_file.write("    .output_z_ack(long_adder_z_ack)\n")
    output_file.write("  );\n\n")
    output_file.write("  \n  always @(posedge clk)\n")
    output_file.write("  begin\n\n")
    output_file.write("    long_adder_done <= 0;\n")
    output_file.write("    case(long_add_state)\n\n")
    output_file.write("      wait_go:\n")
    output_file.write("      begin\n")
    output_file.write("        if (long_adder_go) begin\n")
    output_file.write("          long_add_state <= write_a;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      write_a:\n")
    output_file.write("      begin\n")
    output_file.write("        long_adder_a_stb <= 1;\n")
    output_file.write("        if (long_adder_a_stb && long_adder_a_ack) begin\n")
    output_file.write("          long_adder_a_stb <= 0;\n")
    output_file.write("          long_add_state <= write_b;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      write_b:\n")
    output_file.write("      begin\n")
    output_file.write("        long_adder_b_stb <= 1;\n")
    output_file.write("        if (long_adder_b_stb && long_adder_b_ack) begin\n")
    output_file.write("          long_adder_b_stb <= 0;\n")
    output_file.write("          long_add_state <= read_z;\n")
    output_file.write("        end\n")
    output_file.write("      end\n\n")
    output_file.write("      read_z:\n")
    output_file.write("      begin\n")
    output_file.write("        long_adder_z_ack <= 1;\n")
    output_file.write("        if (long_adder_z_stb && long_adder_z_ack) begin\n")
    output_file.write("          long_adder_z_ack <= 0;\n")
    output_file.write("          long_add_state <= wait_go;\n")
    output_file.write("          long_adder_done <= 1;\n")
    output_file.write("        end\n")
    output_file.write("      end\n")
    output_file.write("    endcase\n")
    output_file.write("    if (rst) begin\n")
    output_file.write("      long_add_state <= wait_go;\n")
    output_file.write("      long_adder_a_stb <= 0;\n")
    output_file.write("      long_adder_b_stb <= 0;\n")
    output_file.write("      long_adder_z_ack <= 0;\n")
    output_file.write("    end\n")
    output_file.write("  end\n\n")

def generate_float_to_int_signals(output_file):
    output_file.write("  reg [31:0] float_to;\n")
    output_file.write("  reg float_to_stb;\n")
    output_file.write("  wire float_to_ack;\n")
    output_file.write("  wire [31:0] to_int;\n")
    output_file.write("  wire to_int_stb;\n")
    output_file.write("  reg to_int_ack;\n")
    output_file.write("  reg [1:0] float_to_int_state;\n")
    output_file.write("  reg float_to_int_go;\n")
    output_file.write("  reg float_to_int_done;\n")

def generate_int_to_float_signals(output_file):
    output_file.write("  reg [31:0] int_to;\n")
    output_file.write("  reg int_to_stb;\n")
    output_file.write("  wire int_to_ack;\n")
    output_file.write("  wire [31:0] to_float;\n")
    output_file.write("  wire to_float_stb;\n")
    output_file.write("  reg to_float_ack;\n")
    output_file.write("  reg [1:0] int_to_float_state;\n")
    output_file.write("  reg int_to_float_go;\n")
    output_file.write("  reg int_to_float_done;\n")

def generate_double_to_long_signals(output_file):
    output_file.write("  reg [63:0] double_to;\n")
    output_file.write("  reg double_to_stb;\n")
    output_file.write("  wire double_to_ack;\n")
    output_file.write("  wire [63:0] to_long;\n")
    output_file.write("  wire to_long_stb;\n")
    output_file.write("  reg to_long_ack;\n")
    output_file.write("  reg [1:0] double_to_long_state;\n")
    output_file.write("  reg double_to_long_go;\n")
    output_file.write("  reg double_to_long_done;\n")

def generate_long_to_double_signals(output_file):
    output_file.write("  reg [63:0] long_to;\n")
    output_file.write("  reg long_to_stb;\n")
    output_file.write("  wire long_to_ack;\n")
    output_file.write("  wire [63:0] to_double;\n")
    output_file.write("  wire to_double_stb;\n")
    output_file.write("  reg to_double_ack;\n")
    output_file.write("  reg [1:0] long_to_double_state;\n")
    output_file.write("  reg long_to_double_go;\n")
    output_file.write("  reg long_to_double_done;\n")

def generate_double_to_float_signals(output_file):
    output_file.write("  reg [63:0] double_to_f;\n")
    output_file.write("  reg double_to_f_stb;\n")
    output_file.write("  wire double_to_f_ack;\n")
    output_file.write("  wire [31:0] d_to_float;\n")
    output_file.write("  wire d_to_float_stb;\n")
    output_file.write("  reg d_to_float_ack;\n")
    output_file.write("  reg [1:0] double_to_float_state;\n")
    output_file.write("  reg double_to_float_go;\n")
    output_file.write("  reg double_to_float_done;\n")

def generate_float_to_double_signals(output_file):
    output_file.write("  reg [31:0] float_to_d;\n")
    output_file.write("  reg float_to_d_stb;\n")
    output_file.write("  wire float_to_d_ack;\n")
    output_file.write("  wire [63:0] f_to_double;\n")
    output_file.write("  wire f_to_double_stb;\n")
    output_file.write("  reg f_to_double_ack;\n")
    output_file.write("  reg [1:0] float_to_double_state;\n")
    output_file.write("  reg float_to_double_go;\n")
    output_file.write("  reg float_to_double_done;\n")

def generate_divider_signals(output_file):
    output_file.write("  reg [31:0] divider_a;\n")
    output_file.write("  reg divider_a_stb;\n")
    output_file.write("  wire divider_a_ack;\n")
    output_file.write("  reg [31:0] divider_b;\n")
    output_file.write("  reg divider_b_stb;\n")
    output_file.write("  wire divider_b_ack;\n")
    output_file.write("  wire [31:0] divider_z;\n")
    output_file.write("  wire divider_z_stb;\n")
    output_file.write("  reg divider_z_ack;\n")
    output_file.write("  reg [1:0] div_state;\n")
    output_file.write("  reg divider_go;\n")
    output_file.write("  reg divider_done;\n")

def generate_multiplier_signals(output_file):
    output_file.write("  reg [31:0] multiplier_a;\n")
    output_file.write("  reg multiplier_a_stb;\n")
    output_file.write("  wire multiplier_a_ack;\n")
    output_file.write("  reg [31:0] multiplier_b;\n")
    output_file.write("  reg multiplier_b_stb;\n")
    output_file.write("  wire multiplier_b_ack;\n")
    output_file.write("  wire [31:0] multiplier_z;\n")
    output_file.write("  wire multiplier_z_stb;\n")
    output_file.write("  reg multiplier_z_ack;\n")
    output_file.write("  reg [1:0] mul_state;\n")
    output_file.write("  reg multiplier_go;\n")
    output_file.write("  reg multiplier_done;\n")

def generate_adder_signals(output_file):
    output_file.write("  reg [31:0] adder_a;\n")
    output_file.write("  reg adder_a_stb;\n")
    output_file.write("  wire adder_a_ack;\n")
    output_file.write("  reg [31:0] adder_b;\n")
    output_file.write("  reg adder_b_stb;\n")
    output_file.write("  wire adder_b_ack;\n")
    output_file.write("  wire [31:0] adder_z;\n")
    output_file.write("  wire adder_z_stb;\n")
    output_file.write("  reg adder_z_ack;\n")
    output_file.write("  reg [1:0] add_state;\n")
    output_file.write("  reg adder_go;\n")
    output_file.write("  reg adder_done;\n")

def generate_long_divider_signals(output_file):
    output_file.write("  reg [63:0] long_divider_a;\n")
    output_file.write("  reg long_divider_a_stb;\n")
    output_file.write("  wire long_divider_a_ack;\n")
    output_file.write("  reg [63:0] long_divider_b;\n")
    output_file.write("  reg long_divider_b_stb;\n")
    output_file.write("  wire long_divider_b_ack;\n")
    output_file.write("  wire [63:0] long_divider_z;\n")
    output_file.write("  wire long_divider_z_stb;\n")
    output_file.write("  reg long_divider_z_ack;\n")
    output_file.write("  reg [1:0] long_div_state;\n")
    output_file.write("  reg long_divider_go;\n")
    output_file.write("  reg long_divider_done;\n")

def generate_long_multiplier_signals(output_file):
    output_file.write("  reg [63:0] long_multiplier_a;\n")
    output_file.write("  reg long_multiplier_a_stb;\n")
    output_file.write("  wire long_multiplier_a_ack;\n")
    output_file.write("  reg [63:0] long_multiplier_b;\n")
    output_file.write("  reg long_multiplier_b_stb;\n")
    output_file.write("  wire long_multiplier_b_ack;\n")
    output_file.write("  wire [63:0] long_multiplier_z;\n")
    output_file.write("  wire long_multiplier_z_stb;\n")
    output_file.write("  reg long_multiplier_z_ack;\n")
    output_file.write("  reg [1:0] long_mul_state;\n")
    output_file.write("  reg long_multiplier_go;\n")
    output_file.write("  reg long_multiplier_done;\n")

def generate_long_adder_signals(output_file):
    output_file.write("  reg [63:0] long_adder_a;\n")
    output_file.write("  reg long_adder_a_stb;\n")
    output_file.write("  wire long_adder_a_ack;\n")
    output_file.write("  reg [63:0] long_adder_b;\n")
    output_file.write("  reg long_adder_b_stb;\n")
    output_file.write("  wire long_adder_b_ack;\n")
    output_file.write("  wire [63:0] long_adder_z;\n")
    output_file.write("  wire long_adder_z_stb;\n")
    output_file.write("  reg long_adder_z_ack;\n")
    output_file.write("  reg [1:0] long_add_state;\n")
    output_file.write("  reg long_adder_go;\n")
    output_file.write("  reg long_adder_done;\n")
