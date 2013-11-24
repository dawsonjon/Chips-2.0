Chips
=====

Introduction
------------

Chips is a fast and simple way to design Logic Devices. You can think of
a Chips design as a network on a chip. Many C Programs are all executing in
parallel, streaming data between each other using fast on-chip connections.

The interface is simple, design components using C, and connect them together
to form a chip using a simple python API. Behind the scenes, chips will comvert
C programs into efficient verilog implementation based on interconnected Finite
State Machines, or custom CPUs.

Test
----
>cd test_suite
>test_c2verilog

Install
-------
>sudo python setup install

To Prepare a Source Distribution
--------------------------------
>python setup sdist
Distribution is contained in ./dist

To Create a Windows Distribution
--------------------------------
>python setup bdist_wininst
