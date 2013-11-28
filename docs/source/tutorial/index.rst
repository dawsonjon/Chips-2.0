Tutorial
========

Download
--------

You can download the `source
<https://github.com/dawsonjon/Chips-2.0/archive/master.zip>`_ from the `GitHub
<http://github.com/dawsonjon/Chips-2.0>`_ homepage. Alternatively clone the
project using git::

    ~$ git clone https://github.com/dawsonjon/Chips-2.0.git


Install
-------

1. First `install Python <http://python.org/download>`_. You need *Python* 2.6 or later, but not *Python* 3.
2. In the Linux console, or the Windows command line (you will need
      administrator priveleges)::

        ~$ cd Chips-2.0
        ~$ python setup.py install

Icarus Verilog
---------------
This example uses the `Icarus Verilog <http://iverilog.icarus.com/>`_
simulator, you will need this installed in your command path to follow this
tutorial.

Create and Test a C component 
-----------------------------

Why not start with a simple example. With your favouraite text editor, create a
file count.c and add the following::
        
        void count(){
                for(i=1; i<=10; i++){
                        report(i);
                }
        }

You can convert C components into Verilog components using the C2Verilog
compiler. The *iverilog* option causes the generated Verilog component to be
compiled using Icarus Verilog. The *run* option causes simulation to be run::

        ~$ c2verilog iverilog run test.c
        1
        2
        3
        4
        5
        6
        7
        8
        9
        10

When a design is reset, execution starts with the last function defined in
the C file. This need not be called *main*. The name of the last function
will be used as the name for the generated Verilog component. The C program will
appear to execute in sequence, although the compiler may execute instructions
concurrently if it does not affect the outcome of the program. This will allow
your component to take advantage of the inherent parallelism present in a hardware
design.

The *report* function is a *built-in* function which is helpful for debug, it
will print the value of a variable on the console dirung simulations, when you
synthesise the design it will be ignored.

This component doesn't have any inputs or outputs, so it isn't going to be very
useful in a real design. You can add inputs and outputs to a components using
function calls with special names. Functions that start with the name *input_*
or *output_* are interpretted as inputs, or outputs respectively.

::

        int temp;
        temp = input_spam(); //reads from an input called spam
        temp = input_eggs(); //reads from an input called eggs
        output_fish(temp);   //writes to an output called fish


Reading or writing from inputs and outputs causes program execution to block
until data is available. This syncronises data tranfers with other components
executing in the same device, this method of passing data beween concurrent
processes is much simpler than the mutex/lock/semaphore mechanisms used in
multithreaded applications.

If you don't want to commit yourself to reading and input and blocking
execution, you can check if data is ready::

        int temp;
        if(ready_spam()){
                temp = input_spam();
        }

There is no equivilent function to check if an output is ready to recieve data,
this could cause deadlocks if both the sending and receiving end were waiting
for one another.

We can now construct some basic hardware components quite simply. Here's a counter for instance::

        void counter(){
                while(1){
                        for(i=1; i<=10; i++){
                                output_out(i);
                        }
                }
        }

We can generate an adder like this::

        void added(){
                while(1){
                        output_z(input_a()+input_b());
                }
        }

Or a divider like this (yes, you can synthesise division)::

        void divider(){
                while(1){
                        output_z(input_a()/input_b());
                }
        }

We can split a stream of data into two identical data streams using a tee function::

        void tee(){
                int temp;
                while(1){
                        temp = input_a();
                        output_y(temp);
                        output_z(temp);
                }
        }

If we want to merge two streams of data, we could interlace them::

        void interlace(){
                int temp;
                while(1){
                        temp = input_a();
                        output_z(temp);
                        temp = input_b();
                        output_z(temp);
                }
        }

or we could prioritise one stream over the other::

        void arbiter(){
                int temp;
                while(1){
                        if( ready_a() ){
                                temp = input_a();
                                output_z(temp);
                        } else if( ready_b() ){
                                temp = input_b();
                                output_z(temp);
                        }
                }
        }



Hello World
-----------

No language would be complete without a "hello world" example::

        >>> from chips import *

        >>> my_chip = Chip(
        ...     Console(
        ...         Sequence(*map(ord, "hello world\n")),
        ...     )
        ... )

        >>> #run a simulation
        >>> my_chip.reset()
        >>> my_chip.execute(100)
        hello world
        hello world
        hello world
        ...

In this example we have made only a few changes:

- ``map(ord, "hello world\n")`` creates a list containing the numeric values of
  the ASCII characters in a string.

- This example introduces a new stream, the *Sequence*. The *Sequence* stream
  outputs each of its arguments in turn, when the arguments are exhausted, the
  *Process* repeats.
 
- A *Printer* is stream is not needed in this example since the stream is
  already a sequence of ASCII values.

Generating VHDL
---------------

Now lets consider how the "hello world" example could be implemented in an
actual device. A first step to implementing a device would be to generate a
VHDL model::

        >>> from chips import *
        >>> from chips.VHDL_plugin import Plugin

        >>> my_chip = Chip(
        ...     Console(
        ...         Sequence(*map(ord, "hello_world\n")),
        ...     )
        ... )

        >>> #generate a VHDL model
        >>> code_generator = Plugin(project_name="hello world")
        >>> my_chip.write_code(code_generator)

The *Chips* library uses plugins to generate output code from models. This
means that new code generators can be added to *Chips* without having to
change the way that hardware is designed and simulated. At present, *Chips*
supports C++ and VHDL code generation, but it is VHDL code that allows
*Chips* to be synthesised. 

The VHDL code generation plugin is found in ``chips.VHDL_plugin`` if you run
this example you should find that a VHDL file called hello_world.vhd has been
generated. 

Take a look through this file. you may find that it is difficult to
understand what is going on. the file isn't meant to be read by humans, *Chips*
treats VHDL as a compatibility layer. *VHDL* is pretty much universally
supported by synthesis tools.  You can run this code in an external VHDL
simulator, but you won't be able to synthesise it into a device because real
hardware devices don't have a concept of a *Console*.

To make this example synthesise, we need to write the characters to some
realisable hardware interface. The *Chips* library provides a *SerialOut*
sink, this provides a simple way to direct the stream of characters to a
serial port::

        >>> from chips import *
        >>> from chips.VHDL_plugin import Plugin

        >>> my_chip = Chip(
        ...     SerialOut(
        ...         Sequence(*map(ord, "hello_world\n")),
        ...     )
        ... )

        >>> #generate a vhdl model
        >>> code_generator = Plugin(project_name="hello world", internal_clock=False, internal_reset=False)
        >>> my_chip.write_code(code_generator)

Now you should have a hello_world.vhd file that you can synthesise in a real
device. By default, SerialOut will assume that you are using a 50 MHz clock and
a baud rate of 115200. If you need something else you can use the clock_rate
and baud_rate arguments to specify what you need. Note that the
*internal_clock* and *internal_reset* parameters have been set to false.
Usually, the VHDL plugin includes a clock and reset in the VHDL model, this
allows a simulation to be run without adding any extra VHDL code for the test
bench. In a real chip however, the clock and reset will usually be derived from
outside the device.

More Streams and Sinks
----------------------

So far we have seen three types of streams, *Counter*, *Sequence* and
*Printer*. *Chips* provides a range of streams. The full documentation for
streams is in the `reference manual`_ but a quick summary is included here:
        
+----------------+-----------------------------------------------------------+
| Stream         | Description                                               |
+================+===========================================================+
| Array()        | An indexable memory with an independent read and write    |
|                | port.                                                     |
+----------------+-----------------------------------------------------------+
| Counter()      | A versatile counter with min, max and step parameters     |
|                |                                                           |
+----------------+-----------------------------------------------------------+
| Decoupler()    | A Decoupler removes stream handshaking.                   |
|                |                                                           |
+----------------+-----------------------------------------------------------+
| Resizer()      | A Resizer changes the width, in bits, of the source       |
|                | stream.                                                   |
+----------------+-----------------------------------------------------------+
| Lookup()       | An indexable Read Only Memory with a single read port.    |
|                |                                                           |
+----------------+-----------------------------------------------------------+
| Fifo()         | Stores data items in a buffer.                            |
|                |                                                           |
+----------------+-----------------------------------------------------------+
| Repeater()     | Yields the same data item repeatedly.                     |
|                |                                                           |
+----------------+-----------------------------------------------------------+
| InPort()       | Yields the value of input port pins.                      |
|                |                                                           |
+----------------+-----------------------------------------------------------+
| SerialIn()     | Yields values from a serial UART.                         |
|                |                                                           |
+----------------+-----------------------------------------------------------+
| Output()       | A stream that is fed by a *Process* (more on this later)  |
|                |                                                           |
+----------------+-----------------------------------------------------------+
| Printer()      | A decimal ASCII representation of the source stream.      |
|                |                                                           |
+----------------+-----------------------------------------------------------+
| HexPrinter()   | A hexadecimal ASCII representation of the source stream.  |
|                |                                                           |
+----------------+-----------------------------------------------------------+
| Scanner()      | yields the value of the decimal ASCII source stream.      |
|                |                                                           |
+----------------+-----------------------------------------------------------+

You can also combine streams using the operators : ``abs, ~, +, -, *, //, %,
<<, >>, &, |, ^, ==, !=, <, <=, >, >=`` on the whole they have the same (or
very similar) meaning as they do in *Python* except that they operate on streams
of data. It is also possible to form an expression from regular integers and
streams, *Chips* will automatically transform an integer into an appropriate
*Repeater* stream. For example ``Counter(0, 9, 1)*2`` is a shorthand for
``Counter(0, 9, 1)*Repeater(2).``

The following table summarises the available sinks:

+----------------+-----------------------------------------------------------+
| Sink           | Description                                               |
+================+===========================================================+
| Response()     | A Response sink allows data to be transfered into         |
|                | Python.                                                   |
+----------------+-----------------------------------------------------------+
| OutPort()      | An OutPort sink outputs a stream of data to I/O port      |
|                | pins.                                                     |
+----------------+-----------------------------------------------------------+
| SerialOut()    | A SerialOut outputs data to a serial UART port.           |
|                |                                                           |
+----------------+-----------------------------------------------------------+
| Asserter()     | An Asserter causes an exception if any data in the        |
|                | source stream is zero.                                    |
+----------------+-----------------------------------------------------------+
| Console()      | A Console outputs data to the simulation console.         |
|                |                                                           |
+----------------+-----------------------------------------------------------+

        .. _`reference manual`: http://dawsonjon.github.com/chips/language_reference/

Types and Bit Width
-------------------

For convenience, the central numerical type in *Chips* is a signed integer with
a fixed number of bits.  This is in contrast to *Python*, where integers have a
potentially infinite width. *Chips* tries to simplify some of the design issues
involved with limited width numbers by doing a lot of the work for you, but it
is not always possible to completely hide these details, so you need to how
things are handled behind the scenes.  

*Chips* will automatically determine the width of a stream whenever possible.
In a *Repeater*, *Counter* or *Lookup*, *Chips* will calculate the number of
bits needed to hold the greatest possible value. This is not possible for
*InPort*, or *Array* streams because the maximum possible value is not known at
compile time. When it is not possible to determine the maximum value, the width
must be specified using the bits parameter.

When streams are combined using operators, the width of the resulting stream
will usually be chosen to handle the maximum possible value in the resulting
stream, though there are some exceptions. Adding two 8 bit streams will result
in a 9 bit stream, multiplying two 8 bit streams will result in a 16 bit
stream. The precise handling of bit widths is documented more  fully in the
`reference manual`_.

You can manually change the width of a stream using the *Resize* stream. Making
a streams smaller in width will result in large values being truncated. Making
a stream larger in width will result in sign extension.

        .. _`reference manual`: http://dawsonjon.github.com/chips/language_reference/


Introducing Processes
---------------------

We have seen how the *Chips* library provides quite a few ready made streams
out of the box. Sometimes these streams won't suite our needs, sometimes we
need to define new operations on streams. Suppose we wanted to double the value
of every data item within in an existing stream, a Counter say. Thats easy,
just use the multiply operator ``Counter(0, 9, 1)*2``. Now suppose that we
wanted to square each data item instead. Not so simple, there is no squaring
operator, or even a power operator for that matter. Thats where the *Process*
comes in::

        >>> from chips import *

        >>> counter = Counter(0, 9, 1)
        >>> temp = Variable(0)#create a temporary variable and initialise it to 0.
        >>> counter_squared_stream = Output()

        >>> p=Process(counter.get_bits()*2,
        ...     Loop(
        ...         counter.read(temp),
        ...         counter_squared_stream.write(temp*temp),
        ...     )
        ... )

        >>> c = Chip(Console(Printer(counter_squared_stream)))
        >>> c.reset()
        >>> c.execute(1000)
        0
        1
        4
        9
        16
        25
        36
        ...


This example demonstrates some of the key features of the *Process*:

- Put it simply, a *Process* is small computer program which can contain loops
  and if statements like any other programming language.  
  
- A *Chip* can contain any number of Process objects, they will all run in
  parallel.  

- Within a *Process*, you can use *Variables* to store data. Each variable can
  only be used within one *Process*, to communicate with another *Process* you
  need to use streams.  

- A *Process* can read from any type of stream, in this example the process is
  reading from a *Counter* stream. Only *Output* streams can be written to.
  
- Streams can only be used for point to point communications. A stream cannot
  be read by more than one *Process*. Likewise, an *Output* stream can only be
  written to by one *Process*.

Process Instructions
--------------------

+-----------------+--------------------------------------------------------+
| Instruction     | Description                                            |
+=================+========================================================+
| Variable()      | A Variable is used within a Process to store data.     |
+-----------------+--------------------------------------------------------+
| Value()         | The Value statement gives a value to the surrounding   |
|                 | Evaluate construct.                                    |
+-----------------+--------------------------------------------------------+
| Evaluate()      | An Evaluate  expression allows a block of statements   |
|                 | to be used as an expression.                           |
+-----------------+--------------------------------------------------------+
| Loop()          | The Loop statement executes instructions repeatedly.   |
+-----------------+--------------------------------------------------------+
| If()            | The If statement conditionally executes                |
|                 | instructions.                                          |
+-----------------+--------------------------------------------------------+
| Break()         | The Break statement causes the flow of control to      |
|                 | immediately exit the loop.                             |
+-----------------+--------------------------------------------------------+
| WaitUs()        | WaitUs causes execution to halt until the next tick    |
|                 | of the microsecond timer.                              |
+-----------------+--------------------------------------------------------+
| Continue()      | The Continue statement causes the flow of control to   |
|                 | immediately jump to the next iteration of the          |
|                 | containing loop.                                       |
+-----------------+--------------------------------------------------------+
| Block()         | The Block statement allows instructions to be nested   |
|                 | into a single statement.                               |
+-----------------+--------------------------------------------------------+
| Output.write()  | This method returns a write instruction that writes a  |
|                 | single data item to the Output stream.                 |
+-----------------+--------------------------------------------------------+
| <stream>.read() | This method returns a read instruction that reads a    |
|                 | single data item from a  stream.                       |
+-----------------+--------------------------------------------------------+
| Variable.set()  | This method returns a set instruction that assigns the |
|                 | value of an expression to a variable.                  |
+-----------------+--------------------------------------------------------+

Bit Width Within a Process
--------------------------

We have already seen how streams are usually sized automatically to handle the
largest possible data value. Inside a *Process* however things are handled
differently. A *Process* has a fixed bit width. The width is the first argument
given to a *Process*. Inside a *Process*, the value of any expression will be
resized the width of the *Process*. When a *Process* reads from a stream, the
value will be truncated or sign extended to the width of the *Process*. It is
important to make sure that the width of a *Process* is sufficiently large.

Hierarchical Design
-------------------

You may be expecting *Chips* to provide some mechanism for hierarchical design.
You might expect that *Chips* would provide a means too group items together to
form re-usable components or modules. A really good design tool would allow you
to parameterise components and modules using generics or templates. *Chips* does
not provide any of these things. It doesn't have to.

The *Python* language itself already provides all these things and more. If you
want to make a reusable component you can simply write a *Python* function:: 

        >>> from chips import *

        >>> def double(input_stream):
        ...     """If you use Python functions to build components you can take
        ...     advantage of docstrings to document your design."""
        ...     
        ...     return input_stream * 2

        >>> c = Chip(
        ...     Console(
        ...         Printer(
        ...             double(
        ...                 Sequence(1, 2, 3)
        ...             )
        ...         )
        ...     )
        ... )

        >>> c.reset()
        >>> c.execute(10)
        2
        4
        6
        2
        ...

Streams from Multiple Sources
-----------------------------

Streams can only be have one source of data and one sink, but it is possible to
combine data from more than one source into a single stream using a *Process*.
The simplest approach is to read a value from each source, and write it to the
destination thus::

        >>> from chips import *

        >>> def simple_arbiter(source_0, source_1):
        ...     """Combine data from two streams into a single stream"""
        ...     temp = Variable(0)
        ...     dest = Output()
        ...     Process(max([source_0.get_bits(), source_1.get_bits()]),
        ...         Loop(
        ...             source_0.read(temp),
        ...             dest.write(temp),
        ...             source_1.read(temp),
        ...             dest.write(temp),
        ...         ),
        ...     )
        ...     return dest

        >>> c = Chip(
        ...    Console(
        ...        Printer(
        ...            simple_arbiter(
        ...                Repeater(1), Repeater(2)
        ...            )
        ...        )
        ...    )
        ... )

        >>> c.reset()
        >>> c.execute(100)
        1
        2
        1
        2
        1
        2
        ...

This type of arbiter will always take an equal number of items from source_0,
and source_1. This may be fine in some applications, but if data were not
available on source_0, data from source_1 would also be blocked. One solution
is to use the *available* method of a stream to test whether data is available
before committing to a blocking read::

        >>> from chips import *

        >>> def non_blocking_arbiter(source_0, source_1):
        ...    """Combine data from two streams into a single stream"""
        ...    temp = Variable(0)
        ...    dest = Output()
        ...    Process(max([source_0.get_bits(), source_1.get_bits()]),
        ...        Loop(
        ...            If(source_0.available(),
        ...                source_0.read(temp),
        ...                dest.write(temp),
        ...            ),
        ...            If(source_1.available(),
        ...                source_1.read(temp),
        ...                dest.write(temp),
        ...            ),
        ...        ),
        ...    )
        ...    return dest
        ... 

        >>> blocked = Output()
        >>> p=Process(8,
        ...     #outputs one value then blocks
        ...     blocked.write(1),
        ... )

        >>> c = Chip(
        ...     Console(
        ...         Printer(
        ...             non_blocking_arbiter(
        ...                 blocked, Repeater(2)
        ...             )
        ...         )
        ...     )
        ... )

        >>> c.reset()
        >>> c.execute(100)
        2
        1
        2
        2
        2
        ...

                

Streams with Multiple Sinks
---------------------------

Sometimes a stream will need to be used in more than one place. A simple
solution is to make a splitter or tee using a *Process*::

        >>> from chips import *

        >>> def tee(source):
        ...     """split data into two streams"""
        ...     temp = Variable(0)
        ...     dest_0 = Output()
        ...     dest_1 = Output()
        ...     Process(source.get_bits(),
        ...         Loop(
        ...             source.read(temp),
        ...             dest_0.write(temp),
        ...             dest_1.write(temp),
        ...         ),
        ...     )
        ...     return dest_0, dest_1

        >>> dest_0, dest_1 = tee(Counter(0, 9, 1))

        >>> c = Chip(
        ...     Console(
        ...         Printer(dest_0),
        ...     ),
        ...     Console(
        ...         Printer(dest_1),
        ...     )
        ... )

        >>> c.reset()
        >>> c.execute(100)
        0
        0
        1
        1
        2
        2
        3
        3
        ...

A Worked Example
----------------

TODO

Further Examples
----------------

The `source distribution`_ contains a number of more involved examples so that
you can see for yourself how more complex hardware designs can be formed from
these simple components.

.. _`source distribution` : https://github.com/downloads/dawsonjon/chips/Chips-0.1.2.tar.gz

