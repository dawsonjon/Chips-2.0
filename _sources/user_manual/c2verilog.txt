c2verilog
=========

For simple designs with only one C component, the simplest way to generate Verilog is by using the c2verilog utility.
The utility accepts C files as input, and generates Verilog files as output.

::

    ~$ c2verilog input_file.c

You may automatically compile the output using Icarus Verilog by adding the
`iverilog` option. You may also run the Icarus Verilog simulation using the
`run` option.

::

    ~$ c2verilog iverilog run input_file.c

You can also influence the way the Verilog is generated. By default, a low area
solution is implemented. If you can specify a design optimised for speed using
the `speed` option.

