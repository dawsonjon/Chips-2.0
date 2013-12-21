#!/usr/bin/env python

import subprocess
from math import pi

try:
    from matplotlib import pyplot
except ImportError:
    print "You need matplotlib to run this script!"
    exit(0)

def test():
    subprocess.call("../c2verilog iverilog run fft.c", shell=True)
    fft_x_re = [float(i) for i in open("fft_x_re")]
    fft_x_im = [float(i) for i in open("fft_x_im")]
    pyplot.plot(fft_x_re, label="fft(x) real")
    pyplot.plot(fft_x_im, label="fft(x) imaginary")
    pyplot.title("FFT impulse response")
    pyplot.xlabel("sample")
    pyplot.legend(loc="upper left")
    pyplot.savefig("../docs/source/examples/images/example_2.png")
    pyplot.show()

def indent(lines):
    return "\n    ".join(lines.splitlines())

def generate_docs():

    documentation = """

Example 2 - Fast Fourier Transform
----------------------------------

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

.. image:: images/example_2.png

"""%indent(open("taylor.c").read())

    document = open("../docs/source/examples/example_2.rst", "w").write(documentation)

test()
generate_docs()
