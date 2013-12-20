#!/usr/bin/env python

import subprocess
from math import pi

try:
    from matplotlib import pyplot
except ImportError:
    print "You need matplotlib to run this script!"
    exit(0)

def test():
    subprocess.call("../c2verilog iverilog run taylor.c", shell=True)
    x = [float(i) for i in open("x")]
    sin_x = [float(i) for i in open("sin_x")]
    cos_x = [float(i) for i in open("cos_x")]
    pyplot.xticks(
        [-pi, -pi/2.0, 0, pi/2.0,  pi],
        [r'$-\pi$', r"$-\pi/2$", r'$0$', r'$\pi/2$', r'$\pi$'])
    pyplot.plot(x, sin_x, label="sin(x)")
    pyplot.plot(x, cos_x, label="cos(x)")
    pyplot.ylim(-1.1, 1.1)
    pyplot.xlim(-1.1 * pi, 1.1 * pi)
    pyplot.title("Trig Functions")
    pyplot.xlabel("x (radians)")
    pyplot.legend(loc="upper left")
    pyplot.savefig("../docs/source/examples/images/example_1.png")
    #pyplot.show()

def indent(lines):
    return "\n    ".join(lines.splitlines())

def generate_docs():

    documentation = """

Example 1 - Approximating trig functions using the Taylor Series
----------------------------------------------------------------

In this example, we calculate an approximation of the cosine functions using
the `Taylor series <http://en.wikipedia.org/wiki/Taylor_series>`_:

.. math::

    \\cos (x) = \\sum_{n=0}^{\\infty} \\frac{(-1)^n}{(2n)!} x^{2n}

A more versatile Cosine function exploit the symetry of the cosine function to
handle negative angles. Angles outside the calculable range are handled by
moving the function in to the range 0 to 2*pi. A Sine function is synthesised
from the cosine function by subtracting pi/2 from the angle. Other trig
functions could be synthesised using trig identities.

.. code-block:: c

    %s

A simple test calulates Sine and Cosine for the range -2*pi to 2*pi.

.. image:: images/example_1.png

"""%indent(open("taylor.c").read())

    document = open("../docs/source/examples/example_1.rst", "w").write(documentation)

test()
generate_docs()
