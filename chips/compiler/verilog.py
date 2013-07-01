#!/usr/bin/env python
"""A C to Verilog compiler"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2013, Jonathan P Dawson"
__version__ = "0.1"

def unique(l):

  """In the absence of set in older python implementations, make list values unique"""

  return dict(zip(l, l)).keys()

def generate_CHIP(input_file, name, frames, output_file, registers, memory_size):

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
  testbench = not inputs and not outputs

  #Do not generate a port in testbench mode
  inports = [
    ("input_" + i, 16) for i in inputs
  ] + [
    ("input_" + i + "_stb", 16) for i in inputs
  ] + [
    ("output_" + i + "_ack", 16) for i in outputs
  ]

  outports = [
    ("output_" + i, 16) for i in outputs
  ] + [
    ("output_" + i + "_stb", 16) for i in outputs
  ] + [
    ("input_" + i + "_ack", 16) for i in inputs
  ]

  #create signals and ports for divider
  division_signals = [
    ("a", 16),
    ("b", 16),
    ("z", 16),
    ("divisor", 16),
    ("dividend", 16),
    ("quotient", 16),
    ("remainder", 16),
    ("count", 5),
    ("state", 2),
    ("stb", 1),
    ("ack", 1),
    ("sign", 1),
  ]

  division_wires = [
    ("difference", 16),
  ]

  division_parameters = [
    ("start", 2, 0),
    ("calculate", 2, 1),
    ("finish", 2, 2),
    ("acknowledge", 2, 3),
  ]

  #create list of signals
  signals = [
    ("timer", 16),
    ("program_counter", len(frames)),
    ("address", 16),
    ("data_out", 16),
    ("data_in", 16),
    ("write_enable", 1),
  ] + [
    ("register_%s"%(register), 16) for register in registers
  ] + [
    ("s_output_" + i + "_stb", 16) for i in outputs
  ] + [
    ("s_output_" + i, 16) for i in outputs
  ] + [
    ("s_input_" + i + "_ack", 16) for i in inputs
  ] + division_signals

  parameters = division_parameters
  wires = division_wires

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
      output_file.write("//input : INPUT_%s:16\n"%i)
  for i in outputs:
      output_file.write("//output : OUTPUT_%s:16\n"%i)
  output_file.write("//source_file : %s\n"%input_file)
  output_file.write("///%s\n"%name.title())
  output_file.write("///%s\n"%"".join(["=" for i in name]))
  output_file.write("///\n")
  output_file.write("///*Created by C2CHIP*\n\n")
  output_file.write("module %s"%name)

  all_ports = [name for name, size in inports + outports]
  if all_ports:
      output_file.write("(")
      output_file.write(",".join(all_ports))
      output_file.write(");\n")
  else:
      output_file.write(";\n")


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

  for name, size in wires:
      write_declaration("  wire      ", name, size)

  for name, size, value in parameters:
      write_declaration("  parameter ", name, size, value)

  memory_size = int(memory_size)
  output_file.write("  reg [15:0] memory [%i:0];\n"%(memory_size-1))

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

      output_file.write("  \ninitial\n")
      output_file.write("  begin\n")
      output_file.write("    rst <= 1'b1;\n")
      output_file.write("    #50 rst <= 1'b0;\n")
      output_file.write("  end\n\n")

      output_file.write("  \ninitial\n")
      output_file.write("  begin\n")
      output_file.write("    clk <= 1'b0;\n")
      output_file.write("    while (1) begin\n")
      output_file.write("      #5 clk <= ~clk;\n")
      output_file.write("    end\n")
      output_file.write("  end\n\n")

  #Generate a state machine to execute the instructions
  binary_operators = ["+", "-", "*", "/", "|", "&", "^", "<<", ">>", "<",">", ">=",
    "<=", "==", "!="]

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
  output_file.write("    if (write_enable == 1'b1) begin\n")
  output_file.write("      memory[address] <= data_in;\n")
  output_file.write("    end\n\n")
  output_file.write("    data_out <= memory[address];\n")
  output_file.write("    write_enable <= 1'b0;\n")
  output_file.write("    program_counter <= program_counter + 1;\n")
  output_file.write("    timer <= 16'h0000;\n\n")
  output_file.write("    case(program_counter)\n\n")

  #A frame is executed in each state
  for location, frame in enumerate(frames):
    output_file.write("      16'd%s:\n"%location)
    output_file.write("      begin\n")
    for instruction in frame:

      if instruction["op"] == "literal":
        output_file.write(
          "        register_%s <= 16'd%s;\n"%(
          instruction["dest"],
          instruction["literal"]&0xffff))

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

      elif instruction["op"] in ["/"] and "left" in instruction:

        output_file.write(
          "        divisor  <= $signed(16'd%i);\n"%(instruction["left"]&0xffff))
        output_file.write(
          "        dividend <= $signed(register_%s);\n"%instruction["srcb"])
        output_file.write(
          "        register_%s <= quotient;\n"%instruction["dest"])
        output_file.write("        stb <= 1'b0;\n")
        output_file.write("        if (ack != 1'b1) begin\n")
        output_file.write("          program_counter <= %s;\n"%location)
        output_file.write("          stb <= 1'b1;\n")
        output_file.write("        end\n")

      elif instruction["op"] in ["/"] and "right" in instruction:

        output_file.write(
          "        divisor  <= $signed(register_%s);\n"%instruction["src"])
        output_file.write(
          "        dividend <= $signed(16'd%i);\n"%(instruction["right"]&0xffff))
        output_file.write(
          "        register_%s <= quotient;\n"%instruction["dest"])
        output_file.write("        stb <= 1'b0;\n")
        output_file.write("        if (ack != 1'b1) begin\n")
        output_file.write("          program_counter <= %s;\n"%location)
        output_file.write("          stb <= 1'b1;\n")
        output_file.write("        end\n")
        output_file.write("        $display(stb);")

      elif instruction["op"] in ["/"]:
        output_file.write(
          "        divisor  <= $signed(register_%s);\n"%instruction["src"])
        output_file.write(
          "        dividend <= $signed(register_%s);\n"%instruction["srcb"])
        output_file.write(
          "        register_%s <= quotient;\n"%instruction["dest"])
        output_file.write("        stb <= 1'b0;\n")
        output_file.write("        if (ack != 1'b1) begin\n")
        output_file.write("          program_counter <= %s;\n"%location)
        output_file.write("          stb <= 1'b1;\n")
        output_file.write("        end\n")

      elif instruction["op"] in binary_operators and "left" in instruction:
        output_file.write(
          "        register_%s <= $signed(16'd%s) %s $signed(register_%s);\n"%(
          instruction["dest"],
          instruction["left"]&0xffff,
          instruction["op"],
          instruction["srcb"]))

      elif instruction["op"] in binary_operators and "right" in instruction:
        output_file.write(
          "        register_%s <= $signed(register_%s) %s $signed(16'd%s);\n"%(
          instruction["dest"],
          instruction["src"],
          instruction["op"],
          instruction["right"] & 0xffff))

      elif instruction["op"] in binary_operators:
        output_file.write(
          "        register_%s <= $signed(register_%s) %s $signed(register_%s);\n"%(
          instruction["dest"],
          instruction["src"],
          instruction["op"],
          instruction["srcb"]))

      elif instruction["op"] == "jmp_if_false":
        output_file.write("        if (register_%s == 16'h0000)\n"%(instruction["src"]));
        output_file.write("          program_counter <= %s;\n"%(instruction["label"]&0xffff))

      elif instruction["op"] == "jmp_if_true":
        output_file.write("        if (register_%s != 16'h0000)\n"%(instruction["src"]));
        output_file.write("          program_counter <= 16'd%s;\n"%(instruction["label"]&0xffff))

      elif instruction["op"] == "jmp_and_link":
        output_file.write("        program_counter <= 16'd%s;\n"%(instruction["label"]&0xffff))
        output_file.write("        register_%s <= 16'd%s;\n"%(
          instruction["dest"], (location+1)&0xffff))

      elif instruction["op"] == "jmp_to_reg":
        output_file.write(
          "        program_counter <= register_%s;\n"%instruction["src"])

      elif instruction["op"] == "goto":
        output_file.write("        program_counter <= 16'd%s;\n"%(instruction["label"]&0xffff))

      elif instruction["op"] == "read":
        output_file.write("        register_%s <= input_%s;\n"%(
          instruction["dest"], instruction["input"]))
        output_file.write("        program_counter <= %s;\n"%location)
        output_file.write("        s_input_%s_ack <= 1'b1;\n"%instruction["input"])
        output_file.write( "       if (s_input_%s_ack == 1'b1 && input_%s_stb == 1'b1) begin\n"%(
          instruction["input"],
          instruction["input"]
        ))
        output_file.write("          s_input_%s_ack <= 1'b0;\n"%instruction["input"])
        output_file.write("          program_counter <= 16'd%s;\n"%(location+1))
        output_file.write("        end\n")

      elif instruction["op"] == "ready":
        output_file.write("        register_%s <= 16'd0;\n"%instruction["dest"])
        output_file.write("        register_%s[0] <= input_%s_stb;\n"%(
          instruction["dest"], instruction["input"]))

      elif instruction["op"] == "write":
        output_file.write("        s_output_%s <= register_%s;\n"%(
          instruction["output"], instruction["src"]))
        output_file.write("        program_counter <= %s;\n"%location)
        output_file.write("        s_output_%s_stb <= 1'b1;\n"%instruction["output"])
        output_file.write(
          "        if (s_output_%s_stb == 1'b1 && output_%s_ack == 1'b1) begin\n"%(
          instruction["output"],
          instruction["output"]
        ))
        output_file.write("          s_output_%s_stb <= 1'b0;\n"%instruction["output"])
        output_file.write("          program_counter <= %s;\n"%(location+1))
        output_file.write("        end\n")

      elif instruction["op"] == "memory_read_request":
        output_file.write(
          "        address <= register_%s;\n"%(instruction["src"])
        )

      elif instruction["op"] == "memory_read":
        output_file.write(
          "        register_%s <= data_out;\n"%(instruction["dest"])
        )

      elif instruction["op"] == "memory_write":
        output_file.write("        address <= register_%s;\n"%(instruction["src"]))
        output_file.write("        data_in <= register_%s;\n"%(instruction["srcb"]))
        output_file.write("        write_enable <= 1'b1;\n")

      elif instruction["op"] == "assert":
        output_file.write( "        if (register_%s == 16'h0000) begin\n"%instruction["src"])
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
        output_file.write(
          '        $display ("%%d (report at line: %s in file: %s)", $signed(register_%s));\n'%(
          instruction["line"],
          instruction["file"],
          instruction["src"],
        ))

      elif instruction["op"] == "stop":
        output_file.write('        $finish;\n')
        output_file.write("        program_counter <= program_counter;\n")
    output_file.write("      end\n\n")

  output_file.write("    endcase\n")

  #Reset program counter and control signals
  output_file.write("    if (rst == 1'b1) begin\n")
  output_file.write("      program_counter <= 0;\n")
  output_file.write("      stb <= 1'b0;\n")
  output_file.write("    end\n")
  output_file.write("  end\n")
  for i in inputs:
    output_file.write("  assign input_%s_ack = s_input_%s_ack;\n"%(i, i))
  for i in outputs:
    output_file.write("  assign output_%s_stb = s_output_%s_stb;\n"%(i, i))
    output_file.write("  assign output_%s = s_output_%s;\n"%(i, i))
  
  output_file.write("\n  //////////////////////////////////////////////////////////////////////////////\n")
  output_file.write("  // SERIAL DIVIDER                                                             \n")
  output_file.write("  //                                                                            \n")
  output_file.write("  // The C input file uses division.                                            \n") 
  output_file.write("  // Division is not directly synthesisable in target hardware.                 \n")
  output_file.write("  // This section of the file implements a serial divider.                      \n")
  output_file.write("  // At present, there is no support for concurrent division at instruction     \n")
  output_file.write("  // level. The division operation takes 18 clock cycles. You should consider   \n")
  output_file.write("  // re-writing the C source file to avoid division if performance is not       \n")
  output_file.write("  // accepteable.                                                               \n\n")

  output_file.write("  always @(posedge clk)\n")
  output_file.write("  begin\n\n")
  output_file.write("    ack <= 1'b0;\n\n")
  output_file.write("    case (state)\n\n")
  output_file.write("      start: begin\n\n")
  output_file.write("        a <= divisor[15]?-divisor:divisor;\n")
  output_file.write("        b <= dividend[15]?-dividend:dividend;\n")
  output_file.write("        remainder <= 15'd0;\n")
  output_file.write("        z <= 15'd0;\n")
  output_file.write("        sign  <= divisor[15] ^ dividend[15];\n")
  output_file.write("        count <= 5'd16;\n\n")
  output_file.write("        if( stb == 1'b1 ) begin\n")
  output_file.write("          state <= calculate;\n")
  output_file.write("        end\n\n")
  output_file.write("      end //start\n\n")
  output_file.write("      calculate: begin\n\n")
  output_file.write("        if( difference[15] == 0 ) begin //if remainder > b\n")
  output_file.write("          z <= z * 2 + 1;\n")
  output_file.write("          remainder <= {difference[14:0], a[15]};\n")
  output_file.write("        end else begin\n")
  output_file.write("          z <= z * 2;\n")
  output_file.write("          remainder <= {remainder[14:0], a[15]};\n")
  output_file.write("        end\n\n")
  output_file.write("        a <= a * 2;\n")
#  output_file.write('        $display("count %d", count);')
#  output_file.write('        $display("remainder %b", remainder);')
#  output_file.write('        $display("a %b", a);')
#  output_file.write('        $display("b %b", b);')
#  output_file.write('        $display("z %b", z);')
  output_file.write("        if( count == 5'd0 ) begin\n")
  output_file.write("          state <= finish;\n")
  output_file.write("        end else begin\n")
  output_file.write("          count <= count - 1;\n")
  output_file.write("        end\n\n")
  output_file.write("      end //calculate\n\n")
  output_file.write("      finish: begin\n\n")
  output_file.write("        quotient <= sign?-z:z;\n")
  output_file.write("        ack      <= 1'b1;\n")
  output_file.write("        state    <= acknowledge;\n\n")
  output_file.write("      end //finish\n\n")
  output_file.write("      acknowledge: begin\n\n")
  output_file.write("        ack      <= 1'b0;\n")
  output_file.write("        state    <= start;\n\n")
  output_file.write("      end //wait\n\n")
  output_file.write("    endcase\n\n")
  output_file.write("    if( rst == 1'b1 ) begin\n")
  output_file.write("      ack   <= 1'b0;\n")
  output_file.write("      state <= start;\n")
  output_file.write("    end //if\n")
  output_file.write("  end\n\n")
  output_file.write("  assign difference = remainder - b;\n\n")
  output_file.write("\nendmodule\n")
