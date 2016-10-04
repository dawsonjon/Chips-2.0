"""

Python API
==========

The Python API provides the ability to build systems from C components. Designs
can be simulated using Python as a rich verification environment. Designs can
be converted into Verilog and targeted to FPGAs using the FPGA vendors
synthesis tools.

.. code-block:: python

    from chips.api.api import *

"""

import os
import itertools
import tempfile
import shutil
import inspect
import textwrap
from chips.compiler.exceptions import C2CHIPError
from chips.compiler.python_model import StopSim
from chips_c import bits_to_float, float_to_bits, bits_to_double, double_to_bits, join_words, high_word, low_word
import chips.compiler.compiler


class Chip:

    """

    Chip
    ----

    A chip is a canvas to which you can add inputs outputs, components and wires. When you
    create a chips all you need to give it is a name.

    .. code-block:: python

        mychip = Chip("mychip")

    The interface to a `Chip` may defined by calling `Input` and `Output`
    objects. Each input and output object is given a name. The name will be
    used in the generated Verilog. While any string can be used for the name,
    if you intend to generate Verilog output, the name should be a valid
    Verilog identifier.

    .. code-block:: python

        Input(mychip, "input_1")
        Input(mychip, "input_2")
        Output(mychip, "output_1")

    The implementation of a chip is defined by creating and instancing
    components. For example a simple adder can be created as follows:

    .. code-block:: python

        #define a component
        adder = Component(C_file = \"\"\"
                input_1 = input("input_1");
                input_2 = input("input_2");
                output_1 = output("output_1");
                void main(){
                    while(1){
                        fputc(fgetc(input_1)+fgetc(input_2), output_1);
                    }
                }
        \"\"\", inline=True)

    The adder can then be instanced, and connected up by calling the adder.
    When an added in instanced, the `inputs` and `outputs` arguments should be
    supplied. These dictionaries specify how the inputs and outputs of the
    component should be connected. The dictionary key should be the
    input/output name, and the value should be an `Input`, `Output` or
    `Wire` instance:

    .. code-block:: python

        #instance a component
        my_adder = adder(
            inputs = {
                "input_1" : input_1,
                "input_2" : input_2,
            },
            outputs = {
                "output_1" : output_1,
            },
        )

    Hierarchical Design
    -------------------

    HDLs provide the ability define new components by connecting components
    together. Chips doesn't provide a means to do this. There's no need. A
    Python function does the job nicely. A function can be used to build a four
    input adder out of 2 input adders for example:

    .. code-block:: python


        def four_input_adder(chip, input_a, input_b, input_c, input_d, output_z):

            adder = Component(C_file = \"\"\"
                    a = input("a");
                    b = input("b");
                    z = output("z");
                    void main(){
                        while(1){
                            fputc(fgetc(a)+fgetc(b), z);
                        }
                    }
            \"\"\", inline=True)

            wire_a = Wire(chip)
            wire_b = Wire(chip)

            adder(mychip,
                inputs = {"a" : input_a, "b" : input_b},
                outputs = {"z" : wire_a})

            adder(mychip,
                inputs = {"a" : input_c, "b" : input_d},
                outputs = {"z" : wire_b})

            adder(mychip,
                inputs = {"a" : wire_a, "b" : wire_b},
                outputs = {"z" : output_z})

        mychip = Chip("mychip")
        input_a = Input(mychip, "a")
        input_b = Input(mychip, "b")
        input_c = Input(mychip, "c")
        input_d = Input(mychip, "d")
        output_z = Output(mychip, "z")
        four_input_adder(mychip, input_a, input_b, input_c, input_d, output_z)


    A diagrammatic representation of the `Chip` is shown below.

    ::

               +-------+       +-------+
               | adder |       | adder |
        A =====>       >=======>       >=====> Z
        B =====>       |       |       |
               +-------+       |       |
                               |       |
               +-------+       |       |
               | adder |       |       |
        C =====>       >=======>       |
        D =====>       |       |       |
               +-------+       +-------+

    Functions provide a means to build more complex components out of simple
    ones, but it doesn't stop there. By providing the basic building blocks,
    you can use all the features of the Python language to build chips.

    Ideas:

        + Create multiple instances using loops.
        + Use tuples, arrays or dictionaries to group wires into more complex structures.
        + Use a GUI interface to customise a components or chips.
        + Build libraries of components using modules or packages.
        + Document designs with docutils or sphinx.

    Simulation
    ----------

    There are two ways to transfer data between the python environment, and the
    `Chip` simulation.

    The first and most flexible method is to subclass the `Input` and `Output`
    classes, overriding the data_source and data_sink methods. By defining your
    own data_source and data_sink methods, you can interface to other Python
    code. Using this method allows the simulation to interact with its
    environment on the fly.

    The second simpler method is to employ the `Stimulus` or `Response`
    classes. These classes are themselves inherited from `Input` and `Output`.
    The `Stimulus` class is provided with a Python sequence object for example
    a list, and iterator or a generator at the time it is created created. The
    `Response` class store data as the simulation progresses, and is itself a
    sequence object.

    It is simple to run the simulation, which should be initiated with a reset:

    .. code-block:: python

        mychip.simulation_reset()

    The simulation can be run for a single cycle:

    .. code-block:: python

        mychip.simulation_step()

    The `simulation_run` method executes the simulation until all processes
    complete (which may not happen):

    .. code-block:: python

        mychip.simulation_run()

    There are a couple of methods to terminate the simulation, by waiting for
    simulation time to elapse, or for a certain amount of output data to be
    accumulated.

    .. code-block:: python


        #run simulation for 1000 cycles
        while mychip.time < 1000:
            mychip.simulation_step()


        #run simulation until 1000 data items are collected
        response = Response(chip, "output", "int")
        while len(response) < 1000:
            mychip.simulation_step()

    Code Generation
    ---------------

    Chips designs can be programmed into FPGAs. Chips uses Verilog as its
    output because it is supported by FPGA vendors build tools. Chips output
    almost will be compatible with any FPGA family. Synthesisable Verilog code
    s generated by calling the `generate_verilog` method.

    .. code-block:: python

        mychip.generate_verilog()

    You can also generate a matching testbench using the `generate_testbench`
    method. You can also specify the simulation run time in clock cycles.

    .. code-block:: python

        mychip.generate_testbench(1000) #1000 clocks

    To compile the design in Icarus Verilog, use the `compile_iverilog` method.
    You can also run the code directly if you pass `True` to the
    `compile_iverilog` function. This is most useful to verify that chips
    components match their native python simulations. In most cases Verilog
    simulations will only be needed to by `Chips` developers.

    .. code-block:: python

        mychip.compile_iverilog(True)

    The generated Verilog code is dependent on the chips_lib.v file which is
    output alongside the synthesisable Verilog.

    """

    def __init__(self, name):
        """

        Synopsis:

            .. code-block:: python

               from chips.api.api import Chip
               Chip(name)

        Description:

           Create a `Chip`.

        Arguments:

          name: The name of the chip

        Returns:

            A `Chip` instance.

        """

        self.name = name
        self.instances = []
        self.wires = []
        self.inputs = {}
        self.outputs = {}
        self.components = {}
        self.sn = 0
        _, self.filename, self.lineno, _, _, _ = inspect.stack()[1]

    def generate_verilog(self):
        """

        Synopsis:

            .. code-block:: python

               chip.generate_verilog(name)

        Description:

            Generate synthesisable Verilog output.

        Arguments:

            None

        Returns:

            None

        """

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
        """

        Synopsis:

            .. code-block:: python

               chip.generate_testbench(stop_clocks=None)

        Description:

            Generate a Verilog testbench.

        Arguments:

            stop_clocks: The number of clock cycles for the simulation to run.

        Returns:

            None

        """

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
        """

        Synopsis:

            .. code-block:: python

               chip.compile_iverilog(run=False)

        Description:

            Compile using the external iverilog simulator.

        Arguments:

            run: (optional) run the simulation.

        Returns:

            None

        """

        files = ["%s.v" % i.component_name for i in self.instances]
        files.append(self.name + ".v")
        files.append(self.name + "_tb.v")
        files.append("chips_lib.v")
        files = " ".join(files)

        os.system("iverilog -o %s %s" % (self.name + "_tb", files))
        if run:
            return os.system("vvp %s" % (self.name + "_tb"))

    def simulation_reset(self):
        """

        Synopsis:

            .. code-block:: python

               chip.simulation_reset()

        Description:

            Reset the simulation.

        Arguments:

            None

        Returns:

            None

        """

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
        """

        Synopsis:

            .. code-block:: python

               chip.simulation_step()

        Description:

            Run the simulation for one cycle.

        Arguments:

            None

        Returns:

            None

        """

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
        """

        Synopsis:

            .. code-block:: python

               chip.simulation_run()

        Description:

            Run the simulation until all processes terminate.

        Arguments:

            None

        Returns:

            None

        """

        # if all instances have reached the end of execution then stop
        try:
            while True:
                self.simulation_step()
        except StopSim:
            return


class Component:

    """

    Component
    ---------

    The Component class defines a new type of component.

    Components are written in C. You can supply the C code as a file name, or
    directly as a string:

    .. code-block:: python

        #Call an external C file
        my_component = Component(C_file="adder.c")

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

    Instances
    ---------

    You can make many instances of a component by "calling" the component. Each
    time you make an instance, you must specify the `Chip` it belongs to, and
    connect up the inputs and outputs of the `Component`.

    """

    def __init__(self, C_file, options={}, inline=False):
        """

        Synopsis:

            .. code-block:: python

               from chips.api.api import VerilogComponent
               VerilogComponent(chip, C_file, V_file, options={}, inline=False)

        Description:

            Create a component using C.

        Arguments:

          chip: The chip to which the input belongs

          C_file: A string containing either the filename of the C code, or the
          C code itself. Filenames are relative to the directory containing the
          Python module that instances the component

          options: Compile options

          inline: When true treat C_file as the source code,
          otherwise treat them as filenames

        Returns:

          A component.

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

        Synopsis:

            .. code-block:: python

               component_instance(chip, inputs, output, parameters={}, debug=False,
               profile=False)

        Description:

            Instance a component.

        Arguments:

          chip: The chip to which the input belongs

          inputs: A dictionary of `Wire` or `Input` mappings.

          outputs: A dictionary of `Wire` or `Output` mappings.

          parameters: An optional dictionary of parameters to substitute into
          the C code.

          debug: (optional) enable debug mode.

          profile: (optional) Boolean enable profiling.

        Returns:

            A component instance.

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
        """
        This is a private function, you shouldn't need to call this directly.
        Use Chip.simulation_reset() instead
        """

        chips.compiler.compiler.comp(
            self.component.C_file,
            self.component.options,
            self.parameters,
            self.sn
        )


class Wire:

    """

    Wire
    ----

    A `Wire` is a point to point connection, a stream, that connects an output
    from one component to the input of another. A `Wire` can only have one
    source of data, and one data sink. When you create a `Wire`, you must tell
    it which `Chip` it belongs to:

    .. code-block:: python

        wire_a = Wire(mychip)
        wire_b = Wire(mychip)

    """

    def __init__(self, chip):
        """
        Synopsis:

            .. code-block:: python

                from chips.api.api import Wire
                Wire(chip)

        Description:

            Create a Wire within a chip.

        Arguments:

          chip: The chip to which the input belongs

        Returns:

            A Wire object.

        """

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
        """
        This is a private function, you shouldn't need to call this directly.
        Use Chip.simulation_reset() instead
        """

        self.q = False

    def simulation_update(self):
        """
        This is a private function, you shouldn't need to call this directly.
        Use Chip.simulation_update() instead
        """

        self.src_rdy = self.next_src_rdy
        self.dst_rdy = self.next_dst_rdy


class Input:

    """

    Input
    -----

    An `Input` takes data from outside the `Chip`, and feeds it into the input
    of a `Component`. When you create an `Input`, you need to specify the
    `Chip` it belongs to, and the name it will be given.

    .. code-block:: python

        input_a = Input(mychip, "A")
        input_b = Input(mychip, "B")
        input_c = Input(mychip, "C")
        input_d = Input(mychip, "D")

    In simulation, the Input calls the `data_source` member function, to model
    an input in simulation, subclass the Input and override the `data_source`
    method:

    .. code-block:: python

        from chips.api.api import Input

        stimulus = iter([1, 2, 3, 4, 5])

        class MyInput(Input):

            def data_source(self):
                return next(stimulus)

    """

    def __init__(self, chip, name):
        """
        Synopsis:

            .. code-block:: python

                from chips.api.api import Input
                Input(chip, name)

        Description:

            Create an `Input` within a `Chip`.

        Arguments:

          chip: The chip to which the input belongs

          name: The name of the input (used in verilog code)

        Returns:

            An `Input` instance.

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
        """
        This is a private function, you shouldn't need to call this directly.
        Use Chip.simulation_reset() instead
        """

        self.src_rdy = True
        self.q = self.data_source()

    def simulation_step(self):
        """
        This is a private function, you shouldn't need to call this directly.
        Use Chip.simulation_step() instead
        """

        self.update_data = self.src_rdy and self.dst_rdy

    def simulation_update(self):
        """
        This is a private function, you shouldn't need to call this directly.
        Use Chip.simulation_update() instead
        """

        self.dst_rdy = self.next_dst_rdy
        if self.update_data:
            self.q = self.data_source()

    def data_source(self):
        """Override this function in your application"""

        pass


class Output:

    """

    Output
    ------

    An `Output` takes data from a `Component` output, and sends it outside the
    `Chip`. When you create an `Output` you must tell it which `Chip` it belongs
    to, and the name it will be given.

    In simulation, the `Output` calls the `data_source` member function, to model
    an output in simulation, subclass the Output and override the `data_sink`
    method:

    .. code-block:: python

        from chips.api.api import Output

        class MyOutput(Output):

            def data_sink(self, data):
                print data

    """

    def __init__(self, chip, name):
        """

        Synopsis:

            .. code-block:: python

                from chips.api.api import Output
                Output(chip, name)

        Description:

            Create an `Output` within a `Chip` .

        Arguments:

          chip: The chip to which the input belongs

          name: The name of the output (used in Verilog code)

        Returns:

            An `Output` instance.

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
        """
        This is a private function, you shouldn't need to call this directly.
        Use Chip.simulation_reset() instead
        """

        pass

    def simulation_step(self):
        """
        This is a private function, you shouldn't need to call this directly.
        Use Chip.simulation_step() instead
        """

        if self.src_rdy and self.dst_rdy:
            self.data_sink(self.q)

    def simulation_update(self):
        """
        This is a private function, you shouldn't need to call this directly.
        Use Chip.simulation_update() instead
        """

        self.src_rdy = self.next_src_rdy

    def data_sink(data):
        """override this function in your application"""

        pass


class Stimulus(Input):

    """

    Stimulus
    --------

    Stimulus is a subclass of Input. A Stimulus input provides a convenient
    means to supply data to the Chips simulation using any python sequence
    object for example a, list, an iterator or a generator.

    .. code-block:: python

        from chips.api.api import Sequence

        mychip = Chip("a chip")
        ...

        Sequence(mychip, "counter", "int", range(1, 100))

        mychip.simulation_reset()
        mychip.simulation_run()

    """

    def __init__(self, chip, name, type_, sequence):
        """
        Synopsis:

            .. code-block:: python

                from chips.api.api import Stimulus
                Stimulus(chip, name, type_, sequence)

        Description:

            Create a `Stimulus` input within a `Chip`.

        Arguments:

          chip: The chip to which the input belongs

          name: The name of the output (used in Verilog code)

          type_: The data type of the stimulus, "int", "long", "float"
          or "double"

          sequence: A sequence object for example a list or an generator function

        Returns:

            A `Stimulus` instance.

        """

        Input.__init__(self, chip, name)
        self.sequence = sequence
        self.type_ = type_
        self.high_word = False
        _, self.filename, self.lineno, _, _, _ = inspect.stack()[1]

    def simulation_reset(self):
        """
        This is a private function, you shouldn't need to call this directly.
        Use Chip.simulation_reset() instead
        """

        self.iterator = itertools.cycle(iter(self.sequence))
        self.high_word = False
        Input.simulation_reset(self)

    def data_source(self):
        """
        This is a private function, you shouldn't need to call this directly.
        """

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
                self.high = high_word(long_word)
                low = low_word(long_word)
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
                self.high = high_word(long_word)
                low = low_word(long_word)
                return low

    def __iter__(self):
        """
        This is a private function, you shouldn't need to call this directly.
        __iter__() provides an iterator like interface so that you can use
        functions like iter(), next() or iterate through with a for loop.
        """

        return iter(self.sequence)

    def __len__(self):
        """
        This is a private function, you shouldn't need to call this directly.
        __len__() allows the len() function to be used.
        """

        return len(self.sequence)


class Response(Output):

    """

    Response
    --------

    Response is a subclass of Output. A Response output provides a convenient
    means to extract data to the Chips simulation. A response behaves as a
    Python iterator.

    .. code-block:: python

        from chips.api.api import Response

        mychip = Chip("a chip")
        ...

        sinx = Response(mychip, "sinx", "int")

        mychip.simulation_reset()
        mychip.simulation_run()

        plot(sinx)

    """

    def __init__(self, chip, name, type_):
        """
        Synopsis:

            .. code-block:: python

                from chips.api.api import Response
                Response(chip, name, type_)

        Description:

            Create a `Response` within a `Chip`

        Arguments:

          chip: The chip to which the input belongs

          name: The name of the output (used in Verilog code)

          type_: The data type of the stimulus, "int", "long", "float"
          or "double"

        Returns:

            A `Response` instance.

        """

        Output.__init__(self, chip, name)
        self.type_ = type_
        self.high_word = False
        _, self.filename, self.lineno, _, _, _ = inspect.stack()[1]

    def simulation_reset(self):
        """
        This is a private function, you shouldn't need to call this directly.
        Use Chip.simulation_reset() instead
        """

        self.l = []
        self.times = []
        Output.simulation_reset(self)
        self.high_word = False

    def data_sink(self, value):
        """
        This is a private function, you shouldn't need to call this directly.
        """

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
        """
        This is a private function, you shouldn't need to call this directly.
        __iter__() provides an iterator like interface so that you can use
        functions like iter(), next() or iterate through with a for loop.
        """

        return iter(self.l)

    def __len__(self):
        """
        This is a private function, you shouldn't need to call this directly.
        __len__() allows the len() function to be used.
        """

        return len(self.l)


class VerilogComponent(Component):

    """

    VerilogComponent
    ----------------

    The VerilogComponent is derived from Component. The VerilogComponent does
    not use the C Compiler to generate the Verilog implementation, but allows
    the user to supply Verilog directly. This is useful on occasions when
    hand-crafted Verilog is needed in a performance critical section, or if
    some pre-existing Verilog code needs to be employed.

    .. code-block:: python

        my_component = Adder(C_file="adder.c", V_file="adder.v")

    """

    def __init__(self, C_file, V_file, options={}, inline=False):
        Component.__init__(self, C_file, options, inline)

        """

        Synopsis:

            .. code-block:: python

               from chips.api.api import VerilogComponent
               VerilogComponent(chip, C_file, V_file, options={}, inline=False)

        Description:

            Create a `VerilogComponent`.

        Arguments:

          chip: The chip to which the input belongs

          C_file: A string containing either the filename of the C code, or the
          C code itself. Filenames are relative to the directory containing the
          Python module that instances the component.

          V_file: A string containing either the filemname of the Verilog code,
          or the Verilog code itself. Filenames are relative to the directory
          containing the Python module instancing the component.

          options: Compile options

          inline: When true treat C_file and V_file as the source code,
          otherwise treat them as filenames

        Returns:

            A `VerilogComponent` .

        """

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

        Synopsis:

            .. code-block:: python

               component_instance(chip, inputs, output, parameters={}, debug=False,
               profile=False)

        Description:

            Create an instance of a `Verilog Component`, connect inputs and
            outputs.

        Arguments:

          chip: The chip to which the input belongs

          inputs: A dictionary of `Wire` or `Input` mappings.

          outputs: A dictionary of `Wire` or `Output` mappings.

          parameters: An optional dictionary of parameters to substitute into
          the C code.

          debug: (optional) enable debug mode.

          profile: (optional) Boolean enable profiling.

        Returns:

            A verilog component instance.

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
        """
        This is a private function, you shouldn't need to call this directly.
        """

        f = open(self.component.V_file)
        f1 = open(self.component_name + ".v", "w")
        f1.write(f.read().format(name=self.component_name))
        f.close()
        f1.close()
