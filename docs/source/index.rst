=================================
Chips - Hardware Design in Python
=================================

What is Chips?
==============

Chips makes FPGA design quicker and easier. Chips isn't an HDL like VHDL or
Verilog, its a different way of doing things. In Chips, you design components
using a simple subset of the C programming language. Theres a Python API to
connect C components together using fast data streams to form complex, parallel
systems all in a single chip. You don't need to worry about clocks, resets,
or timing. You don't need to follow special templates to make your code
synthesisable. All thats done for you!

Features
======== 

Some of the key features include:

        - A fast and simple development environment

        - A free open source solution (MIT license)

        - Automatic generation of synthesizable Verilog

        - Optimize for speed or area

        - Use C and Python software tools to design hardware.


A Quick Taster
==============

::

        lfsr.c:

        //4 bit linear feedback shift register

        void lfsr(){
            int new_bit = 0;
            int shift_register = 1;
            while(1){
         
                 //tap off bit 2 and 3 
                 new_bit=((shift_register >> 0) ^ (shift_register >> 1) ^ new_bit);
         
                 //implement shift register
                 shift_register=((new_bit & 1) << 3) | (shift_register >> 1);
         
                 //4 bit mask
                 shift_register &= 0xf
         
                 //write to stream
                 output_code(shift_register);
             }
        }

        console:

        $ c2verilog iverilog run lfsr.c

        8
        12
        14
        7
        3
        1

Download
========
You can download the `source <https://github.com/dawsonjon/Chips-2.0/archive/master.zip>`_ from the `GitHub <http://github.com/dawsonjon/Chips-2.0>`_ homepage. Alternatively clone the project using git::

    $ git clone https://github.com/dawsonjon/Chips-2.0.git

If you want to give Chips a go in some real hardware, why not try the Digilent Atlys `Demo <https://github.com/dawsonjon/Chips-Demo>`_.
 

Documentation
=============
.. toctree::
   :maxdepth: 2

   introduction/index
   tutorial/index
   language_reference/index
   automatic_code_generation/index
   ip_library/index
   extending_chips/index

News
====

..

Links
=====

- `SciPy`_ Scientific Tools for Python.

- `matplotlib`_ 2D plotting library for Python.

- `Python Imaging Library (PIL)`_ Python Imaging Library adds image processing
  capabilities to Python.

- `MyHDL`_ A Hardware description language based on Python.

.. _`SciPy`: http://scipy.org
.. _`matplotlib`: http://matplotlib.sourceforge.net
.. _`MyHDL`: http://www.myhdl.org
.. _`Python Imaging Library (PIL)`: http://www.pythonware.com/products/pil/


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

