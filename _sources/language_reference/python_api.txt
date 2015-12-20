Python API
==========

The C language provides the ability to define components. The Python API
provides the ability to build systems from C components.

To use the Python API, you must import it.

.. code-block:: python

    from chips.api.api import *

Chip
----

Once you have imported the Python API, you can define a chip. A chip is a
canvas to which you can add inputs outputs, components and wires. When you
create a chips all you need to give it is a name.

.. code-block:: python

    mychip = Chip("mychip")

Wire
----

You can create `Input`, `Output` and `Wires` objects. A `Wire` is a point to point connection, a stream, that connects an output from one component to the input of another. A `Wire` can only have one source of data, and one data sink. When you create a `Wire`, you must tell it which `Chip` it belongs to:

.. code-block:: python

    wire_a = Wire(mychip)
    wire_b = Wire(mychip)

Input
-----

An `Input` takes data from outside the `Chip`, and feeds it into the input of a
`Component`. When you create an `Input`, you need to specify the `Chip` it
belongs to, and the name it will be given.

.. code-block:: python

    input_a = Input(mychip, "A")
    input_b = Input(mychip, "B")
    input_c = Input(mychip, "C")
    input_d = Input(mychip, "D")

Output
------

An `Output` takes data from a `Component` output, and sends it outside the
`Chip`. When you create an `Output` you must tell it which `Chip` it belongs
to, and the name it will be given.

Component
---------

From Python, you can import a C component by specifying the file where it is
defined. When you import a C component it will be compiled.

The C file adder.c defines a two input adder.

.. code-block:: python

    //adder.c

    void adder(){
        while(1){
            output_z(input_a() + input_b());
        }
    }

.. code-block:: python

    adder = Component("source/adder.c")

Instances
---------

You can make many instances of a component by "calling" the component. Each
time you make an instance, you must specify the `Chip` it belongs to, and
connect up the inputs and outputs of the `Component`.

.. code-block:: python
  
    adder(mychip,
        inputs = {"a" : input_a, "b" : input_b},
        outputs = {"z" : wire_a})

    adder(mychip,
        inputs = {"a" : input_c, "b" : input_d},
        outputs = {"z" : wire_b})

    adder(mychip,
        inputs = {"a" : wire_a, "b" : wire_b},
        outputs = {"z" : output_z})

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

Code Generation
---------------

You can generate synthesisable Verilog code for your chip
using the `generate_verilog` method.

.. code-block:: python

    mychip.generate_verilog()

You can also generate a matching testbench using the `generate_testbench`
method. You can also specify the simulation run time in clock cycles.

.. code-block:: python
 
    mychip.generate_testbench(1000) #1000 clocks

To compile the design in Icarus Verilog, use the `compile_iverilog` method. You
can also run the code directly if you pass `True` to the `compile_iverilog`
function.
  
.. code-block:: python

    mychip.compile_iverilog(True)

