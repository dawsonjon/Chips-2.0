Installation
============

Download (github)
-----------------

You can download the 
`source <https://github.com/dawsonjon/Chips-2.0/archive/master.zip>`_ 
from the
`Git Hub <https://github.com/dawsonjon/Chips-2.0>`_ 
homepage. Alternatively clone the project using git::

    ~$ git clone --recursive https://github.com/dawsonjon/Chips-2.0.git

Install from github
-------------------

::

        $ cd Chips-2.0
        $ sudo python setup install


Install from PyPi
-----------------

::

        $ pip-install chips


Icarus Verilog
--------------

Chips can automatically simulate the verilog it generates, to simulate verilog
you will need the `Icarus Verilog <http://iverilog.icarus.com/>`_
        simulator. This will need to be installed in your command path.

C Preprocessor
--------------

Chips uses an external C processor. Make sure you have a c preprocessor `cpp`
installed in your path

Other packages
--------------

While not strictly speaking dependencies, you may want to install the following
packages to use all the libraries and examples:

+ numpy
+ scipy
+ matplotlib
+ pil
+ wxpython

