#!/usr/bin/env python

import subprocess
import atexit
from math import pi
import math
from chips.api.api import *

try:
    import scipy as s
    from scipy.signal import firwin
except ImportError:
    print "You need scipy to run this script!"
    exit(0)

try:
    import numpy as n
except ImportError:
    print "You need numpy to run this script!"
    exit(0)

try:
    from matplotlib import pyplot
except ImportError:
    print "You need matplotlib to run this script!"
    exit(0)

def test():

    #create a chip
    chip = Chip("oscillator_example")

    frequency = Stimulus(chip, "frequency", "float", [30.0 + 20.0 * math.sin(2.0 * pi * i/1024.0) for i in range(1024)])
    #sin output
    sin = Response(chip, "sin", "float", 1024)
    #sin output
    cos = Response(chip, "cos", "float", 1024)
    
    #create a filter component using the C code
    fir_comp = Component("dds.c")

    #add an instance to the chip
    fir_inst_1 = fir_comp(
        chip, 
        inputs = {
            "frequency":frequency,
        },
        outputs = {
            "sin":sin,
            "cos":cos,
        },
        parameters = {
            "N":512,
        },
    )

    #run the simulation
    chip.simulation_reset()
    chip.simulation_run()
        
    #plot the result
    pyplot.plot(list(sin), label = "baseband")
    pyplot.plot(list([math.sin(2.0 * pi * i/1024.0) for i in range(1024)]), label = "modulated")
    pyplot.title("1024 sample FM modulated signal")
    pyplot.ylim(-1.1, 1.1)
    pyplot.xlim(0, 1024)
    pyplot.xlabel("X Sample")
    pyplot.savefig("../docs/source/examples/images/example_7.png")
    pyplot.show()



def indent(lines):
    return "\n    ".join(lines.splitlines())

def generate_docs():

    documentation = """

FM Modulation
--------------

It is often useful in digital hardware to simulate a sin wave numerically. It
is possible to implements a sinusoidal oscillator, without having to calculate
the value of the sinusoid for each sample. A typical approach to this in
hardware is to store within a lookup table a series of values, and to sweep
through those values at a programmable rate. This method relies on a large
amount of memory, and the memory requirements increase rapidly for high
resolutions. It is possible to improve the resolution using techniques such as
interpolation.  

In this example however, an alternative method is employed,
trigonometric recurrence allows us to calculate the sin and cosine of a small
angle just once. From there, subsequent samples can be found using multipliers.


.. code-block:: c

    %s

Conveniently, using this method, both a sin and cosine wave are generated. This
is useful in complex mixers which require a coherent sin and cosine wave. We
can control the frequency of the generated wave by stepping through the
waveform more quickly. If the step rate is received from an input, this can be
used to achieve frequency modulation.

.. image:: images/example_7.png

"""%indent(open("dds.c").read())

    document = open("../docs/source/examples/example_7.rst", "w").write(documentation)

test()
generate_docs()
