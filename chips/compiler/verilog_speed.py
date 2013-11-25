#!/usr/bin/env python
"""A C to Verilog compiler"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2013, Jonathan P Dawson"
__version__ = "0.1"

def unique(l):

    """In the absence of set in older python implementations, make list values unique"""

    return dict(zip(l, l)).keys()

def log2(frames):

    """Integer only algorithm to calculate the number of bits needed to store a number"""

    bits = 1
    power = 2
    while power < frames:
        bits += 1
        power *= 2
    return bits

def to_gray(i):

    """Convert integer to gray code"""

    return (i >> 1) ^ i

def generate_CHIP(input_file,
                  name,
                  frames,
                  output_file,
                  registers,
                  memory_size_2,
                  memory_size_4,
                  initialize_memory,
                  memory_content_2,
                  memory_content_4,
                  no_tb_mode=False):

    """A big ugly function to crunch through all the instructions and generate the CHIP equivilent"""

    #calculate the values of jump locations
    location = 0
    labels = {}
    new_frames = []
    for frame in frames:
        if frame[0]["op"] == "label":
            labels[frame[0]["label"]] = location
        else:
            new_frames.append(frame)
            location += 1
    frames = new_frames

    #substitue real values for labeled jump locations
    for frame in frames:
        for instruction in frame:
            if "label" in instruction:
                instruction["label"]=labels[instruction["label"]]

    #list all inputs and outputs used in the program
    inputs = unique([i["input"] for frame in frames for i in frame if "input" in i])
    outputs = unique([i["output"] for frame in frames for i in frame if "output" in i])
    input_files = unique([i["file_name"] for frame in frames for i in frame if "file_read" == i["op"]])
    output_files = unique([i["file_name"] for frame in frames for i in frame if "file_write" == i["op"]])
    testbench = not inputs and not outputs and not no_tb_mode

    #Do not generate a port in testbench mode
    inports = [
      ("input_" + i, 16) for i in inputs
    ] + [
      ("input_" + i + "_stb", 1) for i in inputs
    ] + [
      ("output_" + i + "_ack", 1) for i in outputs
    ]

    outports = [
      ("output_" + i, 16) for i in outputs
    ] + [
      ("output_" + i + "_stb", 1) for i in outputs
    ] + [
      ("input_" + i + "_ack", 1) for i in inputs
    ]

    #create list of signals
    signals = [
      ("timer", 16),
      ("program_counter", log2(len(frames))),
      ("address_2", 16),
      ("data_out_2", 16),
      ("data_in_2", 16),
      ("write_enable_2", 1),
      ("address_4", 16),
      ("data_out_4", 32),
      ("data_in_4", 32),
      ("write_enable_4", 1),
    ] + [
      ("register_%s"%(register), definition[1]*8) for register, definition in registers.iteritems()
    ] + [
      ("s_output_" + i + "_stb", 16) for i in outputs
    ] + [
      ("s_output_" + i, 16) for i in outputs
    ] + [
      ("s_input_" + i + "_ack", 16) for i in inputs
    ]

    if testbench:
        signals.append(("clk", 1))
        signals.append(("rst", 1))
    else:
        inports.append(("clk", 1))
        inports.append(("rst", 1))

    #output the code in verilog
    output_file.write("//name : %s\n"%name)
    output_file.write("//tag : c components\n")
    for i in inputs:
        output_file.write("//input : input_%s:16\n"%i)
    for i in outputs:
        output_file.write("//output : output_%s:16\n"%i)
    output_file.write("//source_file : %s\n"%input_file)
    output_file.write("///%s\n"%"".join(["=" for i in name]))
    output_file.write("///\n")
    output_file.write("///*Created by C2CHIP*\n\n")


    output_file.write("// Register Allocation\n")
    output_file.write("// ===================\n")
    output_file.write("//   %s   %s   %s  \n"%("Register".center(20), "Name".center(20), "Size".center(20)))
    for register, definition in registers.iteritems():
        register_name, size = definition
        output_file.write("//   %s   %s   %s  \n"%(str(register).center(20), register_name.center(20), str(size).center(20)))

    output_file.write("  \n`timescale 1ns/1ps\n")
    output_file.write("module %s"%name)

    all_ports = [name for name, size in inports + outports]
    if all_ports:
        output_file.write("(")
        output_file.write(",".join(all_ports))
        output_file.write(");\n")
    else:
        output_file.write(";\n")

    output_file.write("  integer file_count;\n")

    input_files = dict(zip(input_files, ["input_file_%s"%i for i, j in enumerate(input_files)]))
    for i in input_files.values():
        output_file.write("  integer %s;\n"%i)

    output_files = dict(zip(output_files, ["output_file_%s"%i for i, j in enumerate(output_files)]))
    for i in output_files.values():
        output_file.write("  integer %s;\n"%i)


    def write_declaration(object_type, name, size, value=None):
        if size == 1:
            output_file.write(object_type)
            output_file.write(name)
            if value is not None:
                output_file.write("= %s'd%s"%(size,value))
            output_file.write(";\n")
        else:
            output_file.write(object_type)
            output_file.write("[%i:0]"%(size-1))
            output_file.write(" ")
            output_file.write(name)
            if value is not None:
                output_file.write("= %s'd%s"%(size,value))
            output_file.write(";\n")

    for name, size in inports:
        write_declaration("  input     ", name, size)

    for name, size in outports:
        write_declaration("  output    ", name, size)

    for name, size in signals:
        write_declaration("  reg       ", name, size)

    memory_size_2 = int(memory_size_2)
    memory_size_4 = int(memory_size_4)
    if memory_size_2:
        output_file.write("  reg [15:0] memory_2 [%i:0];\n"%(memory_size_2-1))
    if memory_size_4:
        output_file.write("  reg [31:0] memory_4 [%i:0];\n"%(memory_size_4-1))

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

    #Generate a state machine to execute the instructions
    binary_operators = ["+", "-", "*", "/", "|", "&", "^", "<<", ">>", "<",">", ">=",
      "<=", "==", "!="]


    if initialize_memory and (memory_content_2 or memory_content_4):

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
        for location, content in memory_content_2.iteritems():
            output_file.write("    memory_2[%s] = %s;\n"%(location, content))
        for location, content in memory_content_4.iteritems():
            output_file.write("    memory_4[%s] = %s;\n"%(location, content))
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
    output_file.write("  // FSM IMPLEMENTAION OF C PROCESS                                             \n")
    output_file.write("  //                                                                            \n")
    output_file.write("  // This section of the file contains a Finite State Machine (FSM) implementing\n")
    output_file.write("  // the C process. In general execution is sequential, but the compiler will   \n")
    output_file.write("  // attempt to execute instructions in parallel if the instruction dependencies\n")
    output_file.write("  // allow. Further concurrency can be achieved by executing multiple C         \n")
    output_file.write("  // processes concurrently within the device.                                  \n")

    output_file.write("  \n  always @(posedge clk)\n")
    output_file.write("  begin\n\n")

    if memory_size_2:
        output_file.write("    //implement memory for 2 byte x n arrays\n")
        output_file.write("    if (write_enable_2 == 1'b1) begin\n")
        output_file.write("      memory_2[address_2] <= data_in_2;\n")
        output_file.write("    end\n")
        output_file.write("    data_out_2 <= memory_2[address_2];\n")
        output_file.write("    write_enable_2 <= 1'b0;\n\n")

    if memory_size_4:
        output_file.write("    //implement memory for 4 byte x n arrays\n")
        output_file.write("    if (write_enable_4 == 1'b1) begin\n")
        output_file.write("      memory_4[address_4] <= data_in_4;\n")
        output_file.write("    end\n")
        output_file.write("    data_out_4 <= memory_4[address_4];\n")
        output_file.write("    write_enable_4 <= 1'b0;\n\n")

    output_file.write("    //implement timer\n")
    output_file.write("    timer <= 16'h0000;\n\n")
    output_file.write("    case(program_counter)\n\n")

    #A frame is executed in each state
    for location, frame in enumerate(frames):
        output_file.write("      16'd%s:\n"%to_gray(location))
        output_file.write("      begin\n")
        output_file.write("        program_counter <= 16'd%s;\n"%to_gray(location+1))
        for instruction in frame:

            if instruction["op"] == "literal":
                output_file.write(
                  "        register_%s <= %s;\n"%(
                  instruction["dest"],
                  instruction["literal"]))

            elif instruction["op"] == "move":
                output_file.write(
                  "        register_%s <= register_%s;\n"%(
                  instruction["dest"],
                  instruction["src"]))

            elif instruction["op"] in ["~"]:
                output_file.write(
                  "        register_%s <= ~register_%s;\n"%(
                  instruction["dest"],
                  instruction["src"]))

            elif instruction["op"] in binary_operators and "left" in instruction:
                if not instruction["signed"]:
                    output_file.write(
                      "        register_%s <= %s %s $unsigned(register_%s);\n"%(
                      instruction["dest"],
                      instruction["left"],
                      instruction["op"],
                      instruction["src"]))
                else:
                    #Verilog uses >>> as an arithmetic right shift
                    if instruction["op"] == ">>":
                        instruction["op"] = ">>>"
                    output_file.write(
                      "        register_%s <= %s %s $signed(register_%s);\n"%(
                      instruction["dest"],
                      instruction["left"],
                      instruction["op"],
                      instruction["src"]))

            elif instruction["op"] in binary_operators and "right" in instruction:
                if not instruction["signed"]:
                    output_file.write(
                      "        register_%s <= $unsigned(register_%s) %s %s;\n"%(
                      instruction["dest"],
                      instruction["src"],
                      instruction["op"],
                      instruction["right"]))
                else:
                    #Verilog uses >>> as an arithmetic right shift
                    if instruction["op"] == ">>":
                        instruction["op"] = ">>>"
                    output_file.write(
                      "        register_%s <= $signed(register_%s) %s %s;\n"%(
                      instruction["dest"],
                      instruction["src"],
                      instruction["op"],
                      instruction["right"]))

            elif instruction["op"] in binary_operators:
                if not instruction["signed"]:
                    output_file.write(
                      "        register_%s <= $unsigned(register_%s) %s $unsigned(register_%s);\n"%(
                      instruction["dest"],
                      instruction["src"],
                      instruction["op"],
                      instruction["srcb"]))
                else:
                    #Verilog uses >>> as an arithmetic right shift
                    if instruction["op"] == ">>":
                        instruction["op"] = ">>>"
                    output_file.write(
                      "        register_%s <= $signed(register_%s) %s $signed(register_%s);\n"%(
                      instruction["dest"],
                      instruction["src"],
                      instruction["op"],
                      instruction["srcb"]))

            elif instruction["op"] == "jmp_if_false":
                output_file.write("        if (register_%s == 0)\n"%(instruction["src"]));
                output_file.write("          program_counter <= %s;\n"%to_gray(instruction["label"]&0xffff))

            elif instruction["op"] == "jmp_if_true":
                output_file.write("        if (register_%s != 0)\n"%(instruction["src"]));
                output_file.write("          program_counter <= 16'd%s;\n"%to_gray(instruction["label"]&0xffff))

            elif instruction["op"] == "jmp_and_link":
                output_file.write("        program_counter <= 16'd%s;\n"%to_gray(instruction["label"]&0xffff))
                output_file.write("        register_%s <= 16'd%s;\n"%(
                  instruction["dest"], to_gray((location+1)&0xffff)))

            elif instruction["op"] == "jmp_to_reg":
                output_file.write(
                  "        program_counter <= register_%s;\n"%instruction["src"])

            elif instruction["op"] == "goto":
                output_file.write("        program_counter <= 16'd%s;\n"%(to_gray(instruction["label"]&0xffff)))

            elif instruction["op"] == "file_read":
                output_file.write("        file_count = $fscanf(%s, \"%%d\\n\", register_%s);\n"%(
                  input_files[instruction["file_name"]], instruction["dest"]))

            elif instruction["op"] == "file_write":
                output_file.write("        $fdisplay(%s, \"%%d\", register_%s);\n"%(
                  output_files[instruction["file_name"]], instruction["src"]))

            elif instruction["op"] == "read":
                output_file.write("        register_%s <= input_%s;\n"%(
                  instruction["dest"], instruction["input"]))
                output_file.write("        program_counter <= %s;\n"%to_gray(location))
                output_file.write("        s_input_%s_ack <= 1'b1;\n"%instruction["input"])
                output_file.write( "       if (s_input_%s_ack == 1'b1 && input_%s_stb == 1'b1) begin\n"%(
                  instruction["input"],
                  instruction["input"]
                ))
                output_file.write("          s_input_%s_ack <= 1'b0;\n"%instruction["input"])
                output_file.write("          program_counter <= 16'd%s;\n"%to_gray(location+1))
                output_file.write("        end\n")

            elif instruction["op"] == "ready":
                output_file.write("        register_%s <= 0;\n"%instruction["dest"])
                output_file.write("        register_%s[0] <= input_%s_stb;\n"%(
                  instruction["dest"], instruction["input"]))

            elif instruction["op"] == "write":
                output_file.write("        s_output_%s <= register_%s;\n"%(
                  instruction["output"], instruction["src"]))
                output_file.write("        program_counter <= %s;\n"%to_gray(location))
                output_file.write("        s_output_%s_stb <= 1'b1;\n"%instruction["output"])
                output_file.write(
                  "        if (s_output_%s_stb == 1'b1 && output_%s_ack == 1'b1) begin\n"%(
                  instruction["output"],
                  instruction["output"]
                ))
                output_file.write("          s_output_%s_stb <= 1'b0;\n"%instruction["output"])
                output_file.write("          program_counter <= %s;\n"%to_gray(location+1))
                output_file.write("        end\n")

            elif instruction["op"] == "memory_read_request":
                output_file.write(
                  "        address_%s <= register_%s;\n"%(
                      instruction["element_size"],
                      instruction["src"])
                )

            elif instruction["op"] == "memory_read_wait":
                pass

            elif instruction["op"] == "memory_read":
                output_file.write(
                  "        register_%s <= data_out_%s;\n"%(
                      instruction["dest"],
                      instruction["element_size"])
                )

            elif instruction["op"] == "memory_write":
                output_file.write("        address_%s <= register_%s;\n"%(
                    instruction["element_size"],
                    instruction["src"])
                )
                output_file.write("        data_in_%s <= register_%s;\n"%(
                    instruction["element_size"],
                    instruction["srcb"])
                )
                output_file.write("        write_enable_%s <= 1'b1;\n"%(
                    instruction["element_size"])
                )

            elif instruction["op"] == "memory_write_literal":
                output_file.write("        address_%s <= 16'd%s;\n"%(
                    instruction["element_size"],
                    instruction["address"])
                )
                output_file.write("        data_in_%s <= %s;\n"%(
                    instruction["element_size"],
                    instruction["value"])
                )
                output_file.write("        write_enable_%s <= 1'b1;\n"%(
                    instruction["element_size"])
                )

            elif instruction["op"] == "assert":
                output_file.write( "        if (register_%s == 0) begin\n"%instruction["src"])
                output_file.write( "          $display(\"Assertion failed at line: %s in file: %s\");\n"%(
                  instruction["line"],
                  instruction["file"]
                ))
                output_file.write( "          $finish_and_return(1);\n")
                output_file.write( "        end\n")

            elif instruction["op"] == "wait_clocks":
                output_file.write("        if (timer < register_%s) begin\n"%instruction["src"])
                output_file.write("          program_counter <= program_counter;\n")
                output_file.write("          timer <= timer+1;\n")
                output_file.write("        end\n")

            elif instruction["op"] == "report":
                if not instruction["signed"]:
                    output_file.write(
                      '        $display ("%%d (report at line: %s in file: %s)", $unsigned(register_%s));\n'%(
                      instruction["line"],
                      instruction["file"],
                      instruction["src"],
                    ))
                else:
                    output_file.write(
                      '        $display ("%%d (report at line: %s in file: %s)", $signed(register_%s));\n'%(
                      instruction["line"],
                      instruction["file"],
                      instruction["src"],
                    ))

            elif instruction["op"] == "stop":
                #If we are in testbench mode stop the simulation
                #If we are part of a larger design, other C programs may still be running
                for file_ in input_files.values():
                    output_file.write("        $fclose(%s);\n"%file_)
                for file_ in output_files.values():
                    output_file.write("        $fclose(%s);\n"%file_)
                if testbench:
                    output_file.write('        $finish;\n')
                output_file.write("        program_counter <= program_counter;\n")
        output_file.write("      end\n\n")

    output_file.write("    endcase\n")

    #Reset program counter and control signals
    output_file.write("    if (rst == 1'b1) begin\n")
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
