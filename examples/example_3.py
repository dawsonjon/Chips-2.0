#!/usr/bin/env python

import subprocess
import atexit
from math import pi

try:
    from matplotlib import pyplot
except ImportError:
    print "You need matplotlib to run this script!"
    exit(0)

children = []
def cleanup():
    for child in children:
        print "Terminating child process"
        child.terminate()
atexit.register(cleanup)

def run_c(file_name):
    process = subprocess.Popen(["../c2verilog", "iverilog", "run", str(file_name)])
    children.append(process)
    process.wait()
    children.remove(process)

def test():
#    run_c("log.c")
    x = [float(i) for i in open("x")]
    e_x = [float(i) for i in open("e_x")]
    log_x = [float(i) for i in open("log_x")]
    pyplot.plot(x, e_x, label="exp(x)")
#    pyplot.plot(x, log_x, label="log(x)")
    pyplot.xlim(0, 10.1)
    pyplot.xlabel("x")
    pyplot.ylabel("f(x)")
    pyplot.savefig("../docs/source/examples/images/example_3.png")
    pyplot.show()

def indent(lines):
    return "\n    ".join(lines.splitlines())

def generate_docs():

    documentation = """

Example 3 - Calculate Sqrt using Newton's Method
------------------------------------------------

In this example, we calculate the sqrt of a number using `Newton's method
<http://en.wikipedia.org/wiki/Newton's_method#Square_root_of_a_number>`_:

Starting with an initial estimate of the sqrt, successively better approximations can be found thus:

.. math::

    f(x_1) = x_0 - \\frac{{x_0}^2 - n}{2x_0}

The function terminates when further iterations do not change the approximation.

.. code-block:: c

    %s

A simple test calulates sqrt(x) where -10 < x < 10.

.. image:: images/example_3.png

"""%indent(open("sqrt.c").read())

    document = open("../docs/source/examples/example_3.rst", "w").write(documentation)

test()
generate_docs()
