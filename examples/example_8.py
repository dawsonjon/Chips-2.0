#!/usr/bin/env python
from chips.api.api import *

try:
    from PIL import Image
except ImportError:
    print "You need Python Imaging Library to run this script!"
    exit(0)

def test():

    im = Image.open("test.bmp")
    image_data = list(im.getdata())
    width, height = im.size
    
    chip = Chip("edge_detection")
    image_in = Stimulus(chip, "image_in", "int", image_data)
    image_out = Response(chip, "image_out", "int", width * height)
    
    #create a filter component using the C code
    fir_comp = Component("edge_detect.c")

    #add an instance to the chip
    fir_inst_1 = fir_comp(
        chip, 
        inputs = {
            "image_in":image_in,
        },
        outputs = {
            "image_out":image_out,
        },
        parameters = {
            "WIDTH":width,
            "HEIGHT":height,
            "SIZE":width * height,
        },
    )

    #run the simulation
    chip.simulation_reset()
    chip.simulation_run()

    #show the result
    new_image = list(image_out)
    new_im = Image.new(im.mode, (width, height))
    new_im.putdata(new_image)
    im.show()
    new_im.show() 
    new_im.save("../docs/source/examples/images/after.bmp") 

def indent(lines):
    return "\n    ".join(lines.splitlines())

def generate_docs():

    documentation = """

Edge Detection
==============

This simple example shows how a simple 3x3 convolution matrix can be used to
perform an *edge detect* operation on a grey-scale image. The convolution matrix
is the "quick mask" matrix presented in `Image Processing in C <http://homepages.inf.ed.ac.uk/rbf/BOOKS/PHILLIPS/cips2ed.pdf>`_ which
also gives a straight forward introduction to edge detection algorithms.

The Python Imaging Library allows real images to be used in the simulation.

.. code-block:: c

    %s


.. image:: images/test.bmp
.. image:: images/after.bmp

"""%indent(open("edge_detect.c").read())

    document = open("../docs/source/examples/example_8.rst", "w").write(documentation)

test()
generate_docs()
