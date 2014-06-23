from chips.compiler.exceptions import C2CHIPError
import chips.compiler.compiler
from chips.compiler.python_model import StopSim
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

    def simulation_reset(self):

        """reset the native python simulation"""

        for instance in self.instances:
            instance.model.simulation_reset()

        for wire in self.wires:
            wire.stb = False
            wire.ack = False

        for input_ in self.inputs:
            input_.stb = False
            input_.ack = False
            input_.simulation_reset()

        for output in self.outputs:
            output.stb = False
            output.ack = False
            output.simulation_reset()

    def simulation_step(self):

        """execute the python simuilation by one step"""

        for instance in self.instances:
            instance.model.simulation_step()

        for input_ in self.inputs:
            input_.simulation_step()

        for output in self.outputs:
            output.simulation_step()

    def simulation_run(self):

        """execute the python simuilation to completion"""

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

    If you want to keep the C file seperate you can read it in from a file like
    this::

        my_component = Adder(C_file="adder.c")

    Once you have defined a component you can use the __call__ method to create
    an instance of the component.

    """

    def __init__(self, C_file, options=[]):

        """Takes a single string argument, the C code to compile"""

        self.name, self.inputs, self.outputs, self.doc = chips.compiler.compiler.comp(C_file, options)
        self.C_file = C_file
        self.options = options

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

    Remember that you can't simulate verilog components using a python model.

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


        #check that correct number of wires have been passed in
        if len(self.component.inputs) != len(self.inputs):
            print "component inputs:"
            for i in self.component.inputs:
                print i
            print "instance inputs:"
            for i in self.inputs:
                print i
            raise C2CHIPError("Instance %s does not have the right number or inputs"%self.component.name)

        if len(self.component.outputs) != len(self.outputs):
            raise C2CHIPError("Instance %s does not have the right number or outputs"%self.component.name)

        #check for multiple sources or sinks
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

        #generate a python simulation model of the instance
        self.model = chips.compiler.compiler.compile_python_model(self.component.C_file, self.component.options, inputs, outputs)


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

    def simulation_reset(self):
        self.data = self.data_source()
        self.write_state = "wait_ack"

    def simulation_step(self):
        if self.write_state == "wait_ack":
            self.stb = True
            if self.ack:
                self.stb = False
                self.write_state = "wait_nack"
        elif self.write_state == "wait_nack":
            if not self.ack:
                self.write_state = "wait_ack"
                self.data = self.data_source()

    def data_source(self):

        """Override this function in your application"""

        pass

class Output:

    """Create an output from the chip."""

    def __init__(self, chip, name):

        """Takes two argument, the chip to which the output belongs, and a
        string representing the name"""

        self.chip = chip
        chip.outputs.append(self)
        self.source = None
        self.name = name

    def simulation_reset(self):
        self.read_state = "wait_stb"

    def simulation_step(self):
        if self.read_state == "wait_stb":
            if self.stb:
                self.ack = True
                self.read_state = "wait_nstb"
                self.data_sink(self.data)
        elif self.read_state == "wait_nstb":
            if not self.stb:
                self.ack = False
                self.read_state = "wait_stb"

    def data_sink(data):

        """override this function in your application"""

        pass
