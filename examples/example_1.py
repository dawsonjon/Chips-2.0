#!/usr/bin/env python2

import subprocess
import atexit
import sys
from math import pi
from chips.api.api import Chip, Stimulus, Response, Wire, Component

try:
    from matplotlib import pyplot
except ImportError:
    print "You need matplotlib to run this script!"
    exit(0)

def test():

    chip = Chip("square_root")

    test_in = Stimulus(chip, "input", "float", [i*0.1 for i in range(100)])
    test_out = Response(chip, "output", "float")
    
    #create a filter component using the C code
    sqrt = Component("sqrt.c")

    #add an instance to the chip
    sqrt(
        chip, 
        inputs = {
            "x":test_in,
        },
        outputs = {
            "sqrt_x":test_out,
        },
    )

    #run the simulation
    chip.simulation_reset()
    while len(test_out) < 100:
        chip.simulation_step()

    pyplot.plot(list(test_in), list(test_out))
    pyplot.xlim(0, 10.1)
    pyplot.title("Square Root of x")
    pyplot.xlabel("x")
    pyplot.ylabel("$\\sqrt{x}$")
    pyplot.savefig("../docs/source/examples/images/example_1.png")
    pyplot.show()

def indent(lines):
    return "\n    ".join(lines.splitlines())

def generate_docs():

    documentation = """

Calculate Square Root using Newton's Method
===========================================

In this example, we calculate the sqrt of a number using `Newton's method
<http://en.wikipedia.org/wiki/Newton's_method#Square_root_of_a_number>`_.
The problem of finding the square root can be expressed as:

.. math::

     n = x^2

Which can be rearranged as:

.. math::

     f(x) = x^2 - n

Using Newton's method, we can find numerically the approximate point at which
:math:`f(x) = 0`. Repeated applications of the following expression yield
increasingly accurate approximations of the Square root:

.. math::

    f(x_k) = x_{k-1} - \\frac{{x_{k-1}}^2 - n}{2x_{k-1}}

Turning this into a practical solution, the following code calculates the square
root of a floating point number. An initial approximation is refined using
Newton's method until further refinements agree to within a small degree.

.. code-block:: c

    %s

Note that the code isn't entirely robust, and cannot handle special cases such
as Nans, infinities or negative numbers.  A simple test calculates
:math:`\\sqrt{x}` where :math:`-10 < x < 10`.

.. image:: images/example_1.png

"""%indent(open("sqrt.c").read())

    document = open("../docs/source/examples/example_1.rst", "w").write(documentation)

test()
generate_docs()
