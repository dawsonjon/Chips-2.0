import os
import itertools
import tempfile
import shutil
import inspect
import textwrap
from chips.compiler.exceptions import C2CHIPError
from chips.compiler.python_model import StopSim
from chips.compiler.utils import float_to_bits, bits_to_float
from chips.compiler.utils import double_to_bits, bits_to_double
from chips.compiler.utils import split_word, join_words
import chips.compiler.compiler


class Chip:

    """

    A Chip represents a collection of components connected together by wires.
    As you create wires and component instances, you will need to tell them
    which chip they belong to. Once you have a completed chip you can:

      + Implement it in verilog - using the generate_verilog method +
      Automatically generate documentation - using the generate_document method

    You can create a new chip like this::

        my_chip = Chip(name = "My Chip")

    """

    def __init__(self, name):
        """Takes a single argument *name*, the name of the chip"""

        self.name = name
        self.instances = []
        self.wires = []
        self.inputs = {}
        self.outputs = {}
        self.components = {}
        self.sn = 0
        _, self.filename, self.lineno, _, _, _ = inspect.stack()[1]

    def generate_verilog(self):
        """Generate verilog for the chip"""

        for component in self.components.values():
            component.generate_verilog()

        for i in self.wires:
            if i.source is None:
                raise C2CHIPError(
                    "wire %s has no source" % i.name, i.filename, i.lineno)
            if i.sink is None:
                raise C2CHIPError(
                    "wire %s has no sink" % i.name, i.filename, i.lineno)

        for i in self.inputs.values():
            if i.sink is None:
                raise C2CHIPError(
                    "input %s has no sink" % i.name, i.filename, i.lineno)

        for i in self.outputs.values():
            if i.source is None:
                raise C2CHIPError(
                    "output %s has no source" % i.name, i.filename, i.lineno)

        ports = ["clk", "rst", "exception"]
        ports += ["%s" % i.name for i in self.inputs.values()]
        ports += ["%s_stb" % i.name for i in self.inputs.values()]
        ports += ["%s_ack" % i.name for i in self.inputs.values()]
        ports += ["%s" % i.name for i in self.outputs.values()]
        ports += ["%s_stb" % i.name for i in self.outputs.values()]
        ports += ["%s_ack" % i.name for i in self.outputs.values()]
        ports = ", ".join(ports)

        output_file = open(self.name + ".v", "w")
        output_file.write("module %s(%s);\n" % (self.name, ports))
        output_file.write("  input  clk;\n")
        output_file.write("  input  rst;\n")
        output_file.write("  output  exception;\n")
        for i in self.inputs.values():
            output_file.write("  input  [31:0] %s;\n" % i.name)
            output_file.write("  input  %s_stb;\n" % i.name)
            output_file.write("  output %s_ack;\n" % i.name)
        for i in self.outputs.values():
            output_file.write("  output [31:0] %s;\n" % i.name)
            output_file.write("  output %s_stb;\n" % i.name)
            output_file.write("  input  %s_ack;\n" % i.name)
        for i in self.wires:
            output_file.write("  wire   [31:0] %s;\n" % i.name)
            output_file.write("  wire   %s_stb;\n" % i.name)
            output_file.write("  wire   %s_ack;\n" % i.name)
        for instance in self.instances:
            output_file.write("  wire   exception_%s;\n" % (id(instance)))
        for instance in self.instances:
            component = instance.component_name
            output_file.write(
                "  %s %s_%s(\n    " % (component, component, id(instance)))
            ports = []
            ports.append(".clk(clk)")
            ports.append(".rst(rst)")
            ports.append(".exception(exception_%s)" % id(instance))
            for name, i in instance.inputs.iteritems():
                ports.append(".input_%s(%s)" % (name, i.name))
                ports.append(".input_%s_stb(%s_stb)" % (name, i.name))
                ports.append(".input_%s_ack(%s_ack)" % (name, i.name))
            for name, i in instance.outputs.iteritems():
                ports.append(".output_%s(%s)" % (name, i.name))
                ports.append(".output_%s_stb(%s_stb)" % (name, i.name))
                ports.append(".output_%s_ack(%s_ack)" % (name, i.name))
            output_file.write(",\n    ".join(ports))
            output_file.write(");\n")
        output_file.write("  assign exception = %s;\n" % (
            " || ".join(["exception_" + str(id(i)) for i in self.instances])
        ))
        output_file.write("endmodule\n")
        output_file.close()

    def generate_testbench(self, stop_clocks=None):
        """Generate verilog for the test bench"""

        output_file = open(self.name + "_tb.v", "w")
        output_file.write("module %s_tb;\n" % self.name)
        output_file.write("  reg  clk;\n")
        output_file.write("  reg  rst;\n")
        for i in self.inputs.values():
            output_file.write("  wire  [31:0] %s;\n" % i.name)
            output_file.write("  wire  %s_stb;\n" % i.name)
            output_file.write("  wire  %s_ack;\n" % i.name)
        for i in self.outputs.values():
            output_file.write("  wire  [31:0] %s;\n" % i.name)
            output_file.write("  wire  %s_stb;\n" % i.name)
            output_file.write("  wire  %s_ack;\n" % i.name)

        output_file.write("  \n  initial\n")
        output_file.write("  begin\n")
        output_file.write("    rst <= 1'b1;\n")
        output_file.write("    #50 rst <= 1'b0;\n")
        output_file.write("  end\n\n")

        if stop_clocks:
            output_file.write("  \n  initial\n")
            output_file.write("  begin\n")
            output_file.write("    #%s $finish;\n" % (10 * stop_clocks))
            output_file.write("  end\n\n")

        output_file.write("  \n  initial\n")
        output_file.write("  begin\n")
        output_file.write("    clk <= 1'b0;\n")
        output_file.write("    while (1) begin\n")
        output_file.write("      #5 clk <= ~clk;\n")
        output_file.write("    end\n")
        output_file.write("  end\n\n")

        output_file.write("  %s uut(\n    " % (self.name))
        ports = []
        ports.append(".clk(clk)")
        ports.append(".rst(rst)")
        for i in self.inputs.values():
            ports.append(".%s(%s)" % (i.name, i.name))
            ports.append(".%s_stb(%s_stb)" % (i.name, i.name))
            ports.append(".%s_ack(%s_ack)" % (i.name, i.name))
        for i in self.outputs.values():
            ports.append(".%s(%s)" % (i.name, i.name))
            ports.append(".%s_stb(%s_stb)" % (i.name, i.name))
            ports.append(".%s_ack(%s_ack)" % (i.name, i.name))
        output_file.write(",\n    ".join(ports))
        output_file.write(");\n")
        output_file.write("endmodule\n")
        output_file.close()

    def compile_iverilog(self, run=False):
        """Compile using the iverilog simulator"""

        files = ["%s.v" % i.component_name for i in self.instances]
        files.append(self.name + ".v")
        files.append(self.name + "_tb.v")
        files.append("chips_lib.v")
        files = " ".join(files)

        os.system("iverilog -o %s %s" % (self.name + "_tb", files))
        if run:
            return os.system("vvp %s" % (self.name + "_tb"))

    def simulation_reset(self):
        """reset the native python simulation"""

        self.time = 0

        for instance in self.instances:
            instance.model.simulation_reset()

        for wire in self.wires:
            wire.stb = False
            wire.ack = False
            wire.simulation_reset()

        for input_ in self.inputs.values():
            input_.stb = False
            input_.ack = False
            input_.simulation_reset()

        for output in self.outputs.values():
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

        for input_ in self.inputs.values():
            input_.simulation_step()

        for output in self.outputs.values():
            output.simulation_step()

        for i in self.inputs.values() + self.outputs.values() + self.wires:
            i.simulation_update()

        self.time += 1

    def simulation_run(self):
        """execute the python simulation to completion"""

        # if all instances have reached the end of execution then stop
        try:
            while True:
                self.simulation_step()
        except StopSim:
            return


class Component:

    """

    The Component class defines a new type of component.

    Components are written in C. You can supply the C code as a file name, or
    directly as a string::

        #Call an external C file
        my_component = Adder(C_file="adder.c")

        #Supply C code directly
        my_component = Adder(C_file=\"\"\"
            unsigned in1 = input("in1");
            unsigned in2 = input("in2");
            unsigned out = input("out");
            void main(){
                while(1){
                    fputc(fgetc(in1) + fgetc(in2), out);
                }
            }
        \"\"\", inline=True)

    Once you have defined a component you can use the __call__ method to create
    an instance of the component::

        ...

        adder_1 = Adder(
            chip,
            inputs = {"in1":a, "in2":b},
            outputs = {"out":z},
            parameters = {}
        )

    """

    def __init__(self, C_file, options={}, inline=False):
        """
        Takes a single string argument, the file name of the C file to compile.
        """

        if inline:
            self.tempdir = tempfile.mkdtemp()
            self.C_file = os.path.join(self.tempdir, "inline_c_file.c")
            f = open(self.C_file, "w")
            f.write(textwrap.dedent(C_file).strip())
            f.close()
        else:
            caller = inspect.stack()[1]
            caller_module = inspect.getmodule(caller[0])
            caller_location = os.path.dirname(caller_module.__file__)
            self.C_file = os.path.join(caller_location, C_file)

        self.options = options

    def __del__(self):
        if hasattr(self, "tempdir"):
            shutil.rmtree(self.tempdir)

    def __call__(self, chip, inputs, outputs,
                 parameters={}, debug=False, profile=False):
        """

        Takes three arguments:

            + chip, the chip that the component instance belongs to.

            + inputs, a list of *Wires* (or *Inputs*) to connect to the
            component inputs

            + outputs, a list of *Wires* (or *Outputs*) to connect to the
            component outputs + parameters, a dictionary of parameters

        """
        return _Instance(
            self,
            chip,
            parameters,
            inputs,
            outputs,
            debug,
            profile
        )


class _Instance:

    """
    This class represents a component instance. You don't normally need to
    create them directly, use the Component.__call__ method.
    """

    def __init__(self, component, chip, parameters,
                 inputs, outputs, debug=False, profile=False):
        self.chip = chip
        self.parameters = parameters
        self.inputs = inputs
        self.outputs = outputs
        self.component = component
        self.chip.instances.append(self)
        self.debug = debug
        self.profile = profile
        self.sn = chip.sn
        chip.sn += 1
        _, self.filename, self.lineno, _, _, _ = inspect.stack()[1]

        # generate a python simulation model of the instance
        ret = chips.compiler.compiler.compile_python_model(
            self.component.C_file,
            self.component.options,
            parameters,
            inputs,
            outputs,
            self.debug,
            self.profile,
            self.sn
        )

        self.model, component_inputs, component_outputs, component_name = ret

        self.component_name = component_name
        if component_name not in chip.components:
            chip.components[component_name] = self

        # check that correct number of wires have been passed in
        if len(component_inputs) != len(self.inputs):
            for i in component_inputs:
                print "component inputs:"
            for i in self.inputs:
                print "instance inputs:"
            raise C2CHIPError(
                "Instance %s does not have the right number or inputs" % (
                    component_name))

        if len(component_outputs) != len(self.outputs):
            raise C2CHIPError(
                "Instance %s does not have the right number or outputs" % (
                    component_name))

        # check for multiple sources or sinks
        for i in inputs.values():
            if i.sink is not None:
                raise C2CHIPError(
                    "%s already has a sink" % i.name, i.filename, i.lineno)
            i.sink = self

        for i in outputs.values():
            if i.source is not None:
                raise C2CHIPError(
                    "%s has already has a source" % (
                        i.name,
                        i.filename,
                        i.lineno))
            i.source = self

        for i in inputs.keys():
            if i not in component_inputs:
                raise C2CHIPError("%s is not an input of component %s" %
                                  (i, component_name), i.filename, i.lineno)

        for i in outputs.keys():
            if i not in component_outputs:
                raise C2CHIPError("%s is not an output of component %s" %
                                  (i, component_name), i.filename, i.lineno)

    def generate_verilog(self):
        chips.compiler.compiler.comp(
            self.component.C_file,
            self.component.options,
            self.parameters,
            self.sn
        )


class Wire:

    """
    Create a connection between two components. A wire is a point to point
    connection with one input and one output.
    """

    def __init__(self, chip):
        self.chip = chip
        chip.wires.append(self)
        self.source = None
        self.sink = None
        self.name = "wire_" + str(id(self))
        self.src_rdy = False
        self.dst_rdy = False
        self.next_src_rdy = False
        self.next_dst_rdy = False
        _, self.filename, self.lineno, _, _, _ = inspect.stack()[1]

    def simulation_reset(self):
        self.q = False

    def simulation_update(self):
        self.src_rdy = self.next_src_rdy
        self.dst_rdy = self.next_dst_rdy


class Input:

    """Create an input to the chip."""

    def __init__(self, chip, name):
        """
        Takes a single argument, the chip to which the input belongs, and a
        string representing the name.
        """

        self.chip = chip
        chip.inputs[name] = self
        self.sink = None
        self.name = name
        self.src_rdy = True
        self.dst_rdy = False
        self.next_dst_rdy = False
        _, self.filename, self.lineno, _, _, _ = inspect.stack()[1]

    def simulation_reset(self):
        self.src_rdy = True
        self.q = self.data_source()

    def simulation_step(self):
        self.update_data = self.src_rdy and self.dst_rdy

    def simulation_update(self):
        self.dst_rdy = self.next_dst_rdy
        if self.update_data:
            self.q = self.data_source()

    def data_source(self):
        """Override this function in your application"""

        pass


class Output:

    """Create an output from the chip."""

    def __init__(self, chip, name):
        """
        Takes two arguments, the chip to which the output belongs, and a
        string representing the name.
        """

        self.chip = chip
        chip.outputs[name] = self
        self.source = None
        self.name = name
        self.src_rdy = False
        self.dst_rdy = True
        self.next_src_rdy = False
        _, self.filename, self.lineno, _, _, _ = inspect.stack()[1]

    def simulation_reset(self):

        pass

    def simulation_step(self):
        if self.src_rdy and self.dst_rdy:
            self.data_sink(self.q)

    def simulation_update(self):
        self.src_rdy = self.next_src_rdy

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
        _, self.filename, self.lineno, _, _, _ = inspect.stack()[1]

    def simulation_reset(self):
        self.iterator = itertools.cycle(iter(self.sequence))
        self.high_word = False
        Input.simulation_reset(self)

    def data_source(self):

        if self.type_ == "int":
            return next(self.iterator)

        elif self.type_ == "long":

            if self.high_word:
                self.high_word = not self.high_word
                word = self.high
                return word
            else:
                self.high_word = not self.high_word
                long_word = next(self.iterator)
                self.high, low = split_word(long_word)
                return low

        elif self.type_ == "float":

            return float_to_bits(next(self.iterator))

        elif self.type_ == "double":

            if self.high_word:
                self.high_word = not self.high_word
                word = self.high
                return word
            else:
                self.high_word = not self.high_word
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
        _, self.filename, self.lineno, _, _, _ = inspect.stack()[1]

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


class VerilogComponent(Component):

    """
    This version of a component allows an existing verilog file to be used
    instead of auto-generating from the C model::

        my_component = Adder(C_file="adder.c", V_file="adder.v")

    """

    def __init__(self, C_file, V_file, options={}, inline=False):
        Component.__init__(self, C_file, options, inline)

        if inline:
            self.V_file = os.path.join(self.tempdir, "inline_v_file.v")
            f = open(self.V_file, "w")
            f.write(textwrap.dedent(V_file).strip())
            f.close()
        else:
            caller = inspect.stack()[1]
            caller_module = inspect.getmodule(caller[0])
            caller_location = os.path.dirname(caller_module.__file__)
            self.V_file = os.path.join(caller_location, V_file)

    def __call__(self, chip, inputs, outputs,
                 parameters={}, debug=False, profile=False):
        """
        Takes three arguments::

            + chip, the chip that the component instance belongs to.

            + inputs, a list of *Wires* (or *Inputs*) to connect to the
            component inputs.

            + outputs, a list of *Wires* (or *Outputs*) to connect to the
            component outputs

            + parameters, a dictionary of parameters

        """

        return _Verilog_Instance(
            self,
            chip,
            parameters,
            inputs,
            outputs,
            debug,
            profile
        )


class _Verilog_Instance(_Instance):

    """This class represents a component instance. You don't normally need to
    create them directly, use the Component.__call__ method."""

    def __init__(self, component, chip, parameters,
                 inputs, outputs, debug=False, profile=False):
        _Instance.__init__(
            self, component, chip, parameters, inputs, outputs, debug, profile)
        _, self.filename, self.lineno, _, _, _ = inspect.stack()[1]

    def generate_verilog(self):
        f = open(self.component.V_file)
        f1 = open(self.component_name + ".v", "w")
        f1.write(f.read().format(name=self.component_name))
        f.close()
        f1.close()
