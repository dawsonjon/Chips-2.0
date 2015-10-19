C Compiler
==========

The heart of Chips is the C compiler and simulator. The C compiler allows
you to define new hardware components using the C language. Components written
in C can be simulated, or converted automatically into Verilog components.
These Verilog components may then be implemented in an FPGA using tools
provided by FPGA vendors.

The C dialect used in Chips has been made as standard as possible. This
section of the manual describes the subset of the C language that is available
in *Chips*.

Types
-----

The following types are available in chips:

        + `char`
        + `int`
        + `long`
        + `unsigned char`
        + `unsigned int`
        + `unsigned long`
        + `float`
        + `double`

A `char` is at least 8 bits wide.  An `int` is at least 32 bits wide.  A `long`
is at least 64 bits wide.

The `float` type is implemented as an IEEE 754 single precision floating point
number. The `double` and `long double` types are implemented as IEEE 754 double
precision floating point numbers. Round-to-zero (ties to even) is the only
supported rounding mode.

Any type may be used to form an array, including `struct` s and arrays. Arrays
may be nested arbitrarily to form arrays of arrays.  `struct` s may be
assigned, passed to and returned from functions.

Arrays may be passed to functions, in this case the array is not copied, but a
reference is passed. Any modification made to the array within the called
function will also be reflected within the calling function.

Missing Features
----------------

Chips is getting close to supporting the whole C language. The following
features have not been done yet.

+ `union` s
+ `enum` s
+ Variadic Functions


Functions
---------

Recursion is permitted, but it should be remembered that memory is at a premium
in FPGAs. It may be better to avoid recursive functions so that the memory
usage can be predicted at compile time.  Only a fixed number of arguments is
supported, optional arguments are not permitted.

Control Structures
------------------

The usual control structures are supported.

Operators
---------

The usual operators are supported.

Stream I/O
----------

The language has been extended to allow components to communicate by sending
data through streams.

To open an input or an output stream use the built in `input` and `output`
functions. These functions accept a string argument identifying the name of the
input or output.  They return a file handle that can be passed to
the `fgetc`, and `fputc` functions to send or receive data. You can also use
the file I/O functions defined in `print.h`, `scan.h` and `stdio.h`.

.. code-block:: c

    unsigned spam = input("spam");
    unsigned eggs = input("eggs");
    unsigned fish = input("fish");
    int temp;
    temp = fgetc(spam); //reads from an input called spam
    temp = fgetc(eggs); //reads from an input called eggs
    fputc(temp, fish);   //writes to an output called fish

Reading or writing from inputs and outputs causes program execution to block
until data is available. If you don't want to commit yourself to reading and
input and blocking execution, you can check if data is ready.

.. code-block:: c

    unsigned spam = input("spam");
    int temp;
    if(ready(spam)){
       temp = fgetc(spam);
    }

There is an equivilent `output_ready` function to check whether an output,
is waiting for data. Care should be taken to avoid deadlocks which might arise
if both the sender and receiver are waiting for the other to be waiting.

Timed Waits
-----------

Timed waits can be achieved using the built-in `wait-clocks` function. The
wait_clocks function accepts a single argument, the numbers of clock cycles to
wait.

.. code-block:: c
    
    wait_clocks(100); //wait for 1 us with 100MHz clock


Debug and Test
--------------

The built in `report` function displays the value of an expression in the
simulation console. *This will have no effect in a synthesised design.*

.. code-block:: c

    int temp = 4;
    report(temp); //prints 4 to console
    report(10); //prints 10 to the console


The built in function assert causes a simulation error if it is passed a zero
value. *The assert function has no effect in a synthesised design.*

.. code-block:: c

    int temp = 5;
    assert(temp); //does not cause an error
    int temp = 0;
    assert(temp); //will cause a simulation error
    assert(2+2==5); //will cause a simulation error

In simulation, you can write values to a file using the built-in `file_write`
function. The first argument is the value to write, and the second argument is
the file to write to. The file will be overwritten when the simulation starts,
and subsequent calls will append a new vale to the end of the file. Each value
will appear in decimal format on a separate line. A file write has no effect in
a synthesised design.

.. code-block:: c

    file_write(1, "simulation_log.txt");
    file_write(2, "simulation_log.txt");
    file_write(3, "simulation_log.txt");
    file_write(4, "simulation_log.txt");

You can also read values from a file during simulation. A simulation error will
occur if there are no more value in the file.

.. code-block:: c

    assert(file_read("simulation_log.txt") == 1);
    assert(file_read("simulation_log.txt") == 2);
    assert(file_read("simulation_log.txt") == 3);
    assert(file_read("simulation_log.txt") == 4);


C Preprocessor
--------------

Chips uses an external C pre-processor, you will need to make sure that Chips
can see the `cpp` command in its command path.

