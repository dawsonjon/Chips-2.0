#!/usr/bin/env python2

import subprocess
import atexit
from math import pi
from chips.api.api import Chip, Stimulus, Response, Wire, Component

try:
    from matplotlib import pyplot
except ImportError:
    print "You need matplotlib to run this script!"
    exit(0)
try:
    from numpy import arange
except ImportError:
    print "You need numpy to run this script!"
    exit(0)

def test():
    run_c("taylor.c")
    x = [float(i) for i in open("x")]
    sin_x = [float(i) for i in open("sin_x")]
    cos_x = [float(i) for i in open("cos_x")]

def test():

    chip = Chip("taylor")

    stimulus = arange(-2*pi, 2.0*pi, pi/25)
    x = Stimulus(chip, "x", "double", stimulus)
    sin_x = Response(chip, "sin_x", "double")
    cos_x = Response(chip, "cos_x", "double")
    
    #create a filter component using the C code
    sqrt = Component("taylor.c")

    #add an instance to the chip
    sqrt(
        chip, 
        inputs = {
            "x":x,
        },
        outputs = {
            "sin_x":sin_x,
            "cos_x":cos_x,
        },
    )

    #run the simulation
    chip.simulation_reset()
    while len(cos_x) < len(x):
        chip.simulation_step()

    x = list(x)
    sin_x = list(sin_x)[:100]
    cos_x = list(cos_x)[:100]

    pyplot.xticks(
        [-2.0*pi, -pi, 0, pi,  2.0*pi],
        [r'$-2\pi$', r"$-\pi$", r'$0$', r'$\pi$', r'$2\pi$'])
    pyplot.plot(x, sin_x, label="sin(x)")
    pyplot.plot(x, cos_x, label="cos(x)")
    pyplot.ylim(-1.1, 1.1)
    pyplot.xlim(-2.2 * pi, 2.2 * pi)
    pyplot.title("Trig Functions")
    pyplot.xlabel("x (radians)")
    pyplot.legend(loc="upper left")
    pyplot.savefig("../docs/source/examples/images/example_2.png")
    pyplot.show()

def indent(lines):
    return "\n    ".join(lines.splitlines())

def generate_docs():

    documentation = """

Approximating Sine and Cosine functions using Taylor Series
===========================================================

In this example, we calculate an approximation of the cosine functions using
the `Taylor series <http://en.wikipedia.org/wiki/Taylor_series>`_:

.. math::

    \\cos (x) = \\sum_{n=0}^{\\infty} \\frac{(-1)^n}{(2n)!} x^{2n}


The following example uses the Taylor Series approximation to generate the Sine
and Cosine functions. Successive terms of the taylor series are calculated
until successive approximations agree to within a small degree. A Sine
function is also synthesised using the identity :math:`sin(x) \\equiv cos(x-\\pi/2)`

.. code-block:: c

    %s

A simple test calculates Sine and Cosine for the range :math:`-2\\pi <= x <= 2\\pi`.

.. image:: images/example_2.png

"""%indent(open("taylor.c").read())

    document = open("../docs/source/examples/example_2.rst", "w").write(documentation)

test()
generate_docs()
