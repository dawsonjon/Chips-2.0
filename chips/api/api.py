from chips.compiler.exceptions import C2CHIPError
import chips.compiler.compiler
import os
import sys

class Chip:

    """A Chip represents a collection of components connected together by
    wires. As you create wires and component instances, you will need to tell
    them which chip they belong to. Once you have a completed chip you can:

      + Implement it in verilog - using the generate_verilog method
      + Automatically generate documentation - using the generate_document method

    You can create a new chip like this::

        my_chip = Chip(name = "My Chip")"""


    def __init__(self, name):

        """Takes a single argument *name*, the name of the chip"""

        self.name = name
        self.instances = []
        self.wires = []
        self.inputs = []
        self.outputs = []
        self.components = []

    def generate_verilog(self):

        """Generate verilog for the chip"""

        for i in self.wires:
            if i.source is None:
                raise C2CHIPError("wire %s has no source"%i.name)
            if i.sink is None:
                raise C2CHIPError("wire %s has no sink"%i.name)

        for i in self.inputs:
            if i.sink is None:
                raise C2CHIPError("input %s has no sink"%i.name)

        for i in self.outputs:
            if i.source is None:
                raise C2CHIPError("output %s has no source"%i.name)

        ports = ["clk", "rst"]
        ports += ["%s"%i.name for i in self.inputs]
        ports += ["%s_stb"%i.name for i in self.inputs]
        ports += ["%s_ack"%i.name for i in self.inputs]
        ports += ["%s"%i.name for i in self.outputs]
        ports += ["%s_stb"%i.name for i in self.outputs]
        ports += ["%s_ack"%i.name for i in self.outputs]
        ports = ", ".join(ports)

        output_file = open(self.name + ".v", "w")
        output_file.write("module %s(%s);\n"%(self.name, ports))
        output_file.write("  input  clk;\n")
        output_file.write("  input  rst;\n")
        for i in self.inputs:
            output_file.write("  input  [31:0] %s;\n"%i.name)
            output_file.write("  input  %s_stb;\n"%i.name)
            output_file.write("  output %s_ack;\n"%i.name)
        for i in self.outputs:
            output_file.write("  output [31:0] %s;\n"%i.name)
            output_file.write("  output %s_stb;\n"%i.name)
            output_file.write("  input  %s_ack;\n"%i.name)
        for i in self.wires:
            output_file.write("  wire   [31:0] %s;\n"%i.name)
            output_file.write("  wire   %s_stb;\n"%i.name)
            output_file.write("  wire   %s_ack;\n"%i.name)
        for instance in self.instances:
            component = instance.component.name
            output_file.write("  %s %s_%s(\n    "%(component, component, id(instance)))
            ports = []
            ports.append(".clk(clk)")
            ports.append(".rst(rst)")
            for name, i in instance.inputs.iteritems():
                ports.append(".input_%s(%s)"%(name, i.name))
                ports.append(".input_%s_stb(%s_stb)"%(name, i.name))
                ports.append(".input_%s_ack(%s_ack)"%(name, i.name))
            for name, i in instance.outputs.iteritems():
                ports.append(".output_%s(%s)"%(name, i.name))
                ports.append(".output_%s_stb(%s_stb)"%(name, i.name))
                ports.append(".output_%s_ack(%s_ack)"%(name, i.name))
            output_file.write(",\n    ".join(ports))
            output_file.write(");\n")
        output_file.write("endmodule\n")
        output_file.close()

    def generate_testbench(self, stop_clocks=None):

        """Generate verilog for the test bench"""

        output_file = open(self.name + "_tb.v", "w")
        output_file.write("module %s_tb;\n"%self.name)
        output_file.write("  reg  clk;\n")
        output_file.write("  reg  rst;\n")
        for i in self.inputs:
            output_file.write("  wire  [31:0] %s;\n"%i.name)
            output_file.write("  wire  %s_stb;\n"%i.name)
            output_file.write("  wire  %s_ack;\n"%i.name)
        for i in self.outputs:
            output_file.write("  wire  [31:0] %s;\n"%i.name)
            output_file.write("  wire  %s_stb;\n"%i.name)
            output_file.write("  wire  %s_ack;\n"%i.name)

        output_file.write("  \n  initial\n")
        output_file.write("  begin\n")
        output_file.write("    rst <= 1'b1;\n")
        output_file.write("    #50 rst <= 1'b0;\n")
        output_file.write("  end\n\n")

        if stop_clocks:
            output_file.write("  \n  initial\n")
            output_file.write("  begin\n")
            output_file.write("    #%s $finish;\n"%(10*stop_clocks))
            output_file.write("  end\n\n")

        output_file.write("  \n  initial\n")
        output_file.write("  begin\n")
        output_file.write("    clk <= 1'b0;\n")
        output_file.write("    while (1) begin\n")
        output_file.write("      #5 clk <= ~clk;\n")
        output_file.write("    end\n")
        output_file.write("  end\n\n")

        output_file.write("  %s uut(\n    "%(self.name))
        ports = []
        ports.append(".clk(clk)")
        ports.append(".rst(rst)")
        for i in self.inputs:
            ports.append(".%s(%s)"%(i.name, i.name))
            ports.append(".%s_stb(%s_stb)"%(i.name, i.name))
            ports.append(".%s_ack(%s_ack)"%(i.name, i.name))
        for i in self.outputs:
            ports.append(".%s(%s)"%(i.name, i.name))
            ports.append(".%s_stb(%s_stb)"%(i.name, i.name))
            ports.append(".%s_ack(%s_ack)"%(i.name, i.name))
        output_file.write(",\n    ".join(ports))
        output_file.write(");\n")
        output_file.write("endmodule\n")
        output_file.close()

    def compile_iverilog(self, run=False):

        """Compile using the Iverilog simulator"""

        files = ["%s.v"%i.name for i in self.components]
        files.append(self.name + ".v")
        files.append(self.name + "_tb.v")
        files.append("chips_lib.v")
        files = " ".join(files)

        os.system("iverilog -o %s %s"%(self.name + "_tb", files))
        if run:
            return os.system("vvp %s"%(self.name + "_tb"))


class Component:

    """You can use the component class to add new components to your chip.
    Components are written in C, and you need to supply the C code for the
    component when you create it. The Chips API will automatically compile the
    C code, and extract the name, inputs, outputs and the documentation from the
    code.

    If you want to keep the C file seperate you can read it in from a file like
    this::

        my_component = Adder(C_file="adder.c")

    Once you have defined a component you can use the __call__ method to create
    an instance of the component.

    """

    def __init__(self, C_file, options=[]):

        """Takes a single string argument, the C code to compile"""

        self.name, self.inputs, self.outputs, self.doc = chips.compiler.compiler.comp(C_file, options)

    def __call__(self, chip, inputs, outputs):

        """Takes three arguments:
            + chip, the chip that the component instance belongs to.
            + inputs, a list of *Wires* (or *Inputs*) to connect to the component inputs
            + outputs, a list of *Wires* (or *Outputs*) to connect to the component outputs"""
        return _Instance(self, chip, inputs, outputs)


class VerilogComponent(Component):

    """You can use the component class to add new components to your chip.
    This version of Component allows components to be written directly in verilog.

        my_component = Adder("adder", inputs = ["a", "b"], outputs = ["z"])

    Once you have defined a component you can use the __call__ method to create
    an instance of the component.

    """

    def __init__(self, name, inputs, outputs, docs):

        """Takes a single string argument, the C code to compile"""

        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.docs = docs


class _Instance:

    """This class represents a component instance. You don't normaly need to
    create them directly, use the Component.__call__ method."""

    def __init__(self, component, chip, inputs, outputs):
        self.chip = chip
        self.inputs = inputs
        self.outputs = outputs
        self.component = component
        self.chip.instances.append(self)
        if component not in chip.components:
            chip.components.append(component)

        if len(self.component.inputs) != len(self.inputs):
            raise C2CHIPError("Instance %s does not have the right number or inputs"%self.name)

        if len(self.component.outputs) != len(self.outputs):
            raise C2CHIPError("Instance %s does not have the right number or outputs"%self.name)

        for i in inputs.values():
            if i.sink is not None:
                raise C2CHIPError("%s allready has a sink"%i.name)
            i.sink = self

        for i in outputs.values():
            if i.source is not None:
                raise C2CHIPError("%s has allready has a source"%i.name)
            i.source = self

        for i in inputs.keys():
            if i not in self.component.inputs:
                raise C2CHIPError("%s is not an input of component %s"%(i, component.name))

        for i in outputs.keys():
            if i not in self.component.outputs:
                raise C2CHIPError("%s has allready has a source %s"%(i, component.name))

    def simulation_reset(self):

        """reset the native python simulation"""

        self.program_counter = 0
        self.registers = {}
        self.memory = {}

    def simulation_step(self):

        """execute the python simuilation by one step"""

        instruction = self.instructions[program_counter]
        src = instruction["src"]
        srcb = instruction["srcb"]
        literal = instruction["literal"]
        program_counter += 1

        if instruction["op"] == "nop":
            pass

        elif instruction["op"] == "literal":
           self.registers[dest] = literal

        elif instruction["op"] == "move":
           self.registers[dest] = self.registers[src]

        elif instruction["op"] == "not":
           self.registers[dest] = ~self.registers[src]

        elif instruction["op"] == "int_to_float":
           f = float(self.registers[src])
           self.registers[dest] = float_to_bits(f)

        elif instruction["op"] == "float_to_int":
           i = bits_to_float(self.registers[src])
           self.registers[dest] = int(i)

        elif instruction["op"] == "long_to_double":
           double = float(join_words(self.register_hi, self.registers[src]))
           self.register_hi, self.registers[dest] = split_words(double_to_bits(double))

        elif instruction["op"] == "double_to_long":
           bits = int(bits_to_double(join_words(self.register_hi, self.registers[src])))
           self.register_hi, self.registers[dest] = split_words(bits)

        elif instruction["op"] == "float_to_double":
           f = bits_to_float(self.registers[src])
           bits = double_to_bits(f)
           self.register_hi, self.registers[dest] = split(bits)

        elif instruction["op"] == "double_to_float":
           double = float(join_words(self.register_hi, self.registers[src]))
           bits = float_to_bits(f)
           self.registers[dest] = bits

        elif instruction["op"] == "load_hi":
           self.register_hi = bits_to_float(self.registers[src])
           self.registerb_hi = bits_to_float(self.registers[srcb])

        elif instruction["op"] == "add":
           lw = self.registers[src] + self.registers[srcb]
           carry, self.registers[dest] = split_word(lw)
           carry &= 1

        elif instruction["op"] == "add_with_carry":
           lw = self.registers[src] + self.registers[srcb] + carry
           carry, self.registers[dest] = split_word(lw)
           carry &= 1

        elif instruction["op"] == "subtract":
           lw = self.registers[src] + (~self.registers[srcb]) + 1
           carry, self.registers[dest] = split_word(lw)
           carry &= 1
           carry ^= 1

        elif instruction["op"] == "subtract_with_carry":
           lw = self.registers[src] + (~self.registers[srcb]) + carry
           carry, self.registers[dest] = split_word(lw)
           carry &= 1
           carry ^= 1

        elif instruction["op"] == "multiply":
           lw = self.registers[src] * self.registers[srcb]
           self.register_hi, self.registers[dest] = split_word(lw)

        elif instruction["op"] == "result_hi":
            self.registers[dest] = self.register_hi

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

        #FIXME - make work with special floating point values
        elif instruction["op"] == "float_file_write":
                output_file.write('          fp_value = (register_1[31]?-1.0:1.0) *\n')
                output_file.write('              (2.0 ** (register_1[30:23]-127.0)) *\n')
                output_file.write('              ({1\'d1, register_1[22:0]} / (2.0**23));\n')
                output_file.write('          $fdisplay (%s, "%%g", fp_value);\n'%(
                  output_files[
                  instruction["file_name"]]))

        elif instruction["op"] == "long_float_file_write":
                output_file.write('          fp_value = $bitstoreal({register_hi, register_1});\n')
                output_file.write('          $fdisplay (%s, "%%g", fp_value);\n'%(
                  output_files[
                  instruction["file_name"]]))

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

        #FIXME - make work with special floating point values
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
           output_file.write('          $display ("%%g (report (float) at line: %s in file: %s)", fp_value);\n'%(
                  instruction["line"],
                  instruction["file"]))

        elif instruction["op"] == "long_float_report":
           output_file.write('          fp_value = $bitstoreal({register_hi, register_1});\n')
           output_file.write('          $display ("%%g (report (double) at line: %s in file: %s)", fp_value);\n'%(
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


class Wire:

    """Create a connection between two components. A wire is a point to point
    connection with one input and one output"""

    def __init__(self, chip):
        self.chip = chip
        chip.wires.append(self)
        self.source = None
        self.sink = None
        self.name = "wire_" + str(id(self))

class Input:

    """Create an input to the chip."""

    def __init__(self, chip, name):

        """Takes a single argument, the chip to which the input belongs, and a
        string representing the name"""

        self.chip = chip
        chip.inputs.append(self)
        self.sink = None
        self.name = name

class Output:

    """Create an output from the chip."""

    def __init__(self, chip, name):

        """Takes two argument, the chip to which the output belongs, and a
        string representing the name"""

        self.chip = chip
        chip.outputs.append(self)
        self.source = None
        self.name = name

def float_to_bits(f):
    value = 0
    for byte in struct.pack(">f", f)
         value <<= 8
         value |= byte 
    return value

def double_to_bits(f):
    value = 0
    for byte in struct.pack(">d", f)
         value <<= 8
         value |= byte 
    return value

def bits_to_float(bits):
    byte_string = (
        chr((bits & 0xff000000) >> 24) +
        chr((bits & 0xff0000) >> 16) +
        chr((bits & 0xff00) >> 8) +
        chr((bits & 0xff))
    )
    return struct.unpack(">f", byte_string)

def bits_to_double(bits):
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
    return struct.unpack(">d", byte_string)

def join_words(hi, lo):
    return (hi << 32) | lo

def split_words(lw):
    return lw >> 32, lw & 0xffffffff
