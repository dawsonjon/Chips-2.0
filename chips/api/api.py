from chips.compiler.exceptions import C2CHIPError
from chips.compiler.python_model import StopSim
from chips.compiler.utils import float_to_bits, bits_to_float, double_to_bits, bits_to_double, split_word, join_words
import chips.compiler.compiler
import os
import sys
import struct
import itertools


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
        self.components = {}

    def generate_verilog(self):

        """Generate verilog for the chip""" 

        for component in self.components.values():
            component.generate_verilog()

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

        ports = ["clk", "rst", "exception"]
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
        output_file.write("  output  exception;\n")
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
            output_file.write("  wire   exception_%s;\n"%(id(instance)))
        for instance in self.instances:
            component = instance.component_name
            output_file.write("  %s %s_%s(\n    "%(component, component, id(instance)))
            ports = []
            ports.append(".clk(clk)")
            ports.append(".rst(rst)")
            ports.append(".exception(exception_%s)"%id(instance))
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
        output_file.write("  assign exception = %s;\n"%(" || ".join(["exception_" + str(id(i)) for i in self.instances])))
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

        files = ["%s.v"%i.component_name for i in self.instances]
        files.append(self.name + ".v")
        files.append(self.name + "_tb.v")
        files.append("chips_lib.v")
        files = " ".join(files)

        os.system("iverilog -o %s %s"%(self.name + "_tb", files))
        if run:
            return os.system("vvp %s"%(self.name + "_tb"))

    def simulation_reset(self):

        """reset the native python simulation"""

        self.time = 0

        for instance in self.instances:
            instance.model.simulation_reset()

        for wire in self.wires:
            wire.stb = False
            wire.ack = False
            wire.simulation_reset()

        for input_ in self.inputs:
            input_.stb = False
            input_.ack = False
            input_.simulation_reset()

        for output in self.outputs:
            output.stb = False
            output.ack = False
            output.simulation_reset()

    def simulation_step(self):

        """execute the python simulation by one step"""

        AllDone = True
        for instance in self.instances:
            try:
                instance.model.simulation_step()
                AllDone = False
            except StopSim:
                pass

        if AllDone:
            raise StopSim

        for input_ in self.inputs:
            input_.simulation_step()

        for output in self.outputs:
            output.simulation_step()

        self.time+=1

    def simulation_run(self):

        """execute the python simulation to completion"""

        #if all instances have reached the end of execution then stop
        try:
            while True:
                self.simulation_step()
        except StopSim:
            return

class Component:

    """You can use the component class to add new components to your chip.
    Components are written in C, and you need to supply the C code for the
    component when you create it. The Chips API will automatically compile the
    C code, and extract the name, inputs, outputs and the documentation from the
    code.

    If you want to keep the C file separate you can read it in from a file like
    this::

        my_component = Adder(C_file="adder.c")

    Once you have defined a component you can use the __call__ method to create
    an instance of the component.

    """

    def __init__(self, C_file, options=[]):

        """Takes a single string argument, the C code to compile"""

        self.C_file = C_file
        self.options = options

    def __call__(self, chip, inputs, outputs, parameters={}, debug=False, profile=False):

        """Takes three arguments:
            + chip, the chip that the component instance belongs to.
            + inputs, a list of *Wires* (or *Inputs*) to connect to the component inputs
            + outputs, a list of *Wires* (or *Outputs*) to connect to the component outputs
            + parameters, a dictionary of parameters"""
        return _Instance(self, chip, parameters, inputs, outputs, debug, profile)


class _Instance:

    """This class represents a component instance. You don't normaly need to
    create them directly, use the Component.__call__ method."""

    def __init__(self, component, chip, parameters, inputs, outputs, debug=False, profile=False):
        self.chip = chip
        self.parameters = parameters
        self.inputs = inputs
        self.outputs = outputs
        self.component = component
        self.chip.instances.append(self)
        self.debug=debug
        self.profile=profile

        #generate a python simulation model of the instance
        self.model, component_inputs, component_outputs, component_name = chips.compiler.compiler.compile_python_model(
                self.component.C_file, 
                self.component.options, 
                parameters,
                inputs,
                outputs, 
                self.debug,
                self.profile
                )

        self.component_name = component_name
        if component_name not in chip.components:
            chip.components[component_name] = self

        #check that correct number of wires have been passed in
        if len(component_inputs) != len(self.inputs):
            print "component inputs:"
            for i in component_inputs:
                print i
            print "instance inputs:"
            for i in self.inputs:
                print i
            raise C2CHIPError("Instance %s does not have the right number or inputs"%component_name)

        if len(component_outputs) != len(self.outputs):
            raise C2CHIPError("Instance %s does not have the right number or outputs"%component_name)

        #check for multiple sources or sinks
        for i in inputs.values():
            if i.sink is not None:
                raise C2CHIPError("%s already has a sink"%i.name)
            i.sink = self

        for i in outputs.values():
            if i.source is not None:
                raise C2CHIPError("%s has already has a source"%i.name)
            i.source = self

        for i in inputs.keys():
            if i not in component_inputs:
                raise C2CHIPError("%s is not an input of component %s"%(i, component_name))

        for i in outputs.keys():
            if i not in component_outputs:
                raise C2CHIPError("%s has allready has a source %s"%(i, component_name))

    def generate_verilog(self):
        print self.component.C_file
        chips.compiler.compiler.comp(self.component.C_file, self.component.options, self.parameters)



class Wire:

    """Create a connection between two components. A wire is a point to point
    connection with one input and one output"""

    def __init__(self, chip):
        self.chip = chip
        chip.wires.append(self)
        self.source = None
        self.sink = None
        self.name = "wire_" + str(id(self))

    def simulation_reset(self):
        self.q = []

class Input:

    """Create an input to the chip."""

    def __init__(self, chip, name):

        """Takes a single argument, the chip to which the input belongs, and a
        string representing the name"""

        self.chip = chip
        chip.inputs.append(self)
        self.sink = None
        self.name = name

    def simulation_reset(self):
        self.q = [self.data_source()]

    def simulation_step(self):
        if not self.q:
            self.q.append(self.data_source())

    def data_source(self):

        """Override this function in your application"""

        pass

class Output:

    """Create an output from the chip."""

    def __init__(self, chip, name):

        """Takes two arguments, the chip to which the output belongs, and a
        string representing the name"""

        self.chip = chip
        chip.outputs.append(self)
        self.source = None
        self.name = name

    def simulation_reset(self):
        self.q = []

    def simulation_step(self):
        if self.q:
            self.data_sink(self.q.pop(0))

    def data_sink(data):

        """override this function in your application"""

        pass

class Stimulus(Input):

    """Simulate a chip input using a sequence object"""

    def __init__(self, chip, name, type_, sequence):
        Input.__init__(self, chip, name)
        self.sequence = sequence
        self.type_ = type_
        self.high_word = False
       
    def simulation_reset(self):
        self.iterator = itertools.cycle(iter(self.sequence))
        self.high_word = False
        Input.simulation_reset(self)

    def data_source(self):

        if self.type_ == "int":
            return next(self.iterator)

        elif self.type_ == "long":

            if self.high_word:
                self.high_word  = not self.high_word
                word = self.high
                return word
            else:
                self.high_word  = not self.high_word
                long_word = next(self.iterator)
                self.high, low = split_word(long_word)
                return low

        elif self.type_ == "float":

            return float_to_bits(next(self.iterator))

        elif self.type_ == "double":

            if self.high_word:
                self.high_word  = not self.high_word
                word = self.high
                return word
            else:
                self.high_word  = not self.high_word
                long_word = double_to_bits(next(self.iterator))
                self.high, low = split_word(long_word)
                return low

    def __iter__(self):

        """Make a Stimulus work as a sequence"""

        return iter(self.sequence)

    def __len__(self):

        """Make a Stimulus work with the len() function"""

        return len(self.sequence)

class Response(Output):

    """Capture output values during a simulation"""

    def __init__(self, chip, name, type_):
        Output.__init__(self, chip, name)
        self.type_ = type_
        self.high_word = False

    def simulation_reset(self):
        self.l = []
        self.times = []
        Output.simulation_reset(self)
        self.high_word = False
       
    def data_sink(self, value):

        if self.type_ == "int":

            self.l.append(value)
            self.times.append(self.chip.time)

        elif self.type_ == "long":


            if self.high_word:
                self.high_word = not self.high_word
                self.l.append(join_words(value, self.low))
                self.times.append(self.chip.time)
            else:
                self.high_word = not self.high_word
                self.low = value

        elif self.type_ == "float":

            self.l.append(bits_to_float(value))
            self.times.append(self.chip.time)

        elif self.type_ == "double":

            if self.high_word:
                self.high_word = not self.high_word
                self.l.append(bits_to_double(join_words(value, self.low)))
                self.times.append(self.chip.time)
            else:
                self.high_word = not self.high_word
                self.low = value

    def __iter__(self):
        return iter(self.l)

    def __len__(self):
        return len(self.l)
