Introduction
============

*Chips* is a high level, FPGA design tool inspired by *Python*.

Design components in C, design FPGAs in Python
----------------------------------------------

In Chips, a design resembles a network of computers implemented in a single
chip. A chip consists of many interconnected components operating in parallel.
Each component acts like a computer running a C program. 

Components communicate with each other sending messages across buses. The
design of a chip - the components and the connections between them - is carried
out programatically in Python. 

Chips come in three parts:

1. A Python library to build and simulate chips by connecting together digital components using high speed buses.

2. A collection of ready made digital components.

3. A C-to-hardware compiler to make new digital components in the C programming language.

Work at a higher level of abstraction 
-------------------------------------

In Chips, the details of gates, clocks, resets, finite-state machines and
flow-control are handled by the tool, this leaves the designer free to think
about the architecture and the algorithms. This has some benefits:

+ Designs are simpler.
+ Simpler designs take much less time to get working.
+ Simpler designs are much less likely to have bugs.

With Chips the batteries *are* included 
---------------------------------------

With traditional Hardware Description Languages, there are many restrictions on
what can be translated into hardware and implemented in a chip.

With Chips almost all legal code can be translated into hardware. This includes
division, single and double precision IEEE floating point, maths functions,
trig-functions, timed waits, pseudo-random numbers and recursive function
calls.

Python is a rich verification environment
-----------------------------------------

Chips provides the ability to simulate designs natively in Python.  Python is
an excellent programming language with extensive libraries covering many
application domains. This makes it the perfect environment to verify a chip.

`NumPy <http://www.numpy.org/>`_ , `SciPy <http://scipy.org/>`_  and
`MatPlotLib <http://http://matplotlib.org/>`_  will be of interest to
engineers, but thats just the `start <https://pypi.python.org/pypi>`_ .

Try it out
----------

Why not try the `Chips <http://dawsonjon.pythonanywhere.com>`_ web app. 
