class ChipsError(Exception)
    pass

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

    def generate_verilog(self):

        """Generate verilog for the chip"""

        for i in self.wires:
            if i.source is None:
                raise ChipsError("wire %s has no source"%i.name)
            if i.sink is None:
                raise ChipsError("wire %s has no sink"%i.name)

        for i in self.inputs:
            if i.sink is None:
                raise ChipsError("input %s has no sink"%i.name)

        for i in self.outputs:
            if i.source is None:
                raise ChipsError("output %s has no source"%i.name)

        output_file = open(name + ".v")
        output_file.write("module %s;\n"%self.name)
        for i in inputs:
            output_file.write("  input  [15:0] %s;\n"%i.name)
            output_file.write("  input  [15:0] %s_stb;\n"%i.name)
            output_file.write("  output [15:0] %s_ack;\n"%i.name)
        for i in outputs:
            output_file.write("  output [15:0] %s;\n"%i.name)
            output_file.write("  output [15:0] %s_stb;\n"%i.name)
            output_file.write("  input  [15:0] %s_ack;\n"%i.name)
        for i in wires:
            output_file.write("  wire   [15:0] %s;\n"%i.name)
            output_file.write("  wire   [15:0] %s_stb;\n"%i.name)
            output_file.write("  wire   [15:0] %s_ack;\n"%i.name)
        for instance in self.instances:
            component = instance.component.name
            output_file.write("  module %s_%s %s(\n"%(id(instancce), component, component))
            ports = []
            for i in instance.inputs:
                ports.append(i.name)
                ports.append(i.name + "_stb")
                ports.append(i.name + "_ack")
            for i in instance.outputs:
                ports.append(i.name)
                ports.append(i.name + "_stb")
                ports.append(i.name + "_ack")
            output_file.write(",\n    ".join(ports))
            output_file.write(");\n")
        output_file.write("endmodule\n")
        output_file.close()


class Component:

    """You can use the component class to add new components to your chip.
    Components are written in C, and you need to supply the C code for the
    component when you create it. The Chips API will automatically compile the
    C code, and extract the name, inputs, outputs and the documentation from the
    code.
    
    You can create a component like this::

        my_component = Component(C_code = \"\"\"
            int adder(){ //The component name will be adder
                output_z(input_a + input_b); //This will create inputs a, and b, and outputs z.
            }\"\"\"
        )

    If you want to keep the C file seperate you can read it in from a file like
    this::

        my_component = Adder(C_code = open(adder.c).read())

    Once you have defined a component you can use the __call__ method to create
    an instance of the component.
    
    """

    def __init__(self, C_code):

        """Takes a single string argument, the C code to compile"""

        self.name, self.inputs, self.outputs, self.doc = compiler.compiler(C_code)

    def __call__(self, chip, inputs, outputs):

        """Takes three arguments:
            + chip, the chip that the component instance belongs to.
            + inputs, a list of *Wires* (or *Inputs*) to connect to the component inputs
            + outputs, a list of *Wires* (or *Outputs*) to connect to the component outputs"""
        return _Instance(self, chip, inputs, output)


class _Instance:

    """This class represents a component instance. You don't normaly need to
    create them directly, use the Component.__call__ method."""
    
    def __init__(self, component, chip, inputs, outputs):
        self.chip = chip
        self.inputs = inputs
        self.outputs = outputs
        self.component = component
        self.name, self.input_ports, self.output_ports, self.doc = compiler.compiler(C_code)
        self.chip.instances.append(self)

        if len(self.input_ports) != len(self.inputs):
            raise ChipsError("Instance %s does not have the right number or inputs"%self.name)

        if len(self.output_ports) != len(self.outputs):
            raise ChipsError("Instance %s does not have the right number or outputs"%self.name)

        for i in inputs:
            if i.source is not None:
                raise ChipsError("%s allready has a source"%i.name)
            i.sink = self

        for i in outputs:
            if i.sink is not None:
                raise ChipsError("%s has allready has a sink"%i.name)
            i.soure = self

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
