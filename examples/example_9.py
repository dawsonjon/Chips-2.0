#!/usr/bin/env python
from chips.api.api import *
from chips.api.gui import GuiChip
from math import ceil, log

try:
    from PIL import Image
except ImportError:
    print "You need Python Imaging Library to run this script!"
    exit(0)

def test():

    chip = GuiChip("Test Chip")
    test_in = Stimulus(chip, "test_in", "int", [1, 2, 3])
    wire = Wire(chip)
    test_out = Response(chip, "test_out", "int")
    
    #create a filter component using the C code
    compressor = Component("pro.c")
    decompressor = Component("mpress.c")

    #add an instance to the chip
    compressor(
        chip, 
        inputs = {
            "in":test_in,
        },
        outputs = {
            "out":wire,
        },
        parameters = {
        },
    )

    #add an instance to the chip
    decompressor(
        chip, 
        inputs = {
            "in":wire,
        },
        outputs = {
            "out":test_out,
        },
        parameters = {
        },
    )

    #run the simulation
    chip.simulation_reset()
    while len(test_out) < 1024:
        chip.simulation_step()


    #show the result
    print len(test_in)
    print "".join(map(chr, list(test_in)[:1024]))
    print len(test_out)
    print "".join(map(chr, list(test_out)[:1024]))
    print list(test_in)[:1024] == list(test_out)[:1024]

def indent(lines):
    return "\n    ".join(lines.splitlines())

def generate_docs():

    documentation = """

LZSS Compression
================

LZSS is a simple form of of run length compression that exploits repeated
sequences in a block of data. The encoder scans a block of data, and sends
literal characters. However if the encoder encounters a sequence of characters
that have already been sent, it will substitute the sequence with a
reference to the earlier data. The encoder will always select the longest
matching sequence that it has already sent. To achieve this the encoder
needs to store a number of previously sent characters in a buffer. This buffer
is referred to as the window.

.. code-block:: c

    %s

The encoding is simple. A bit is sent to indicate whether a raw character or a
reference continues. A reference consists of a distance length pair. The
distance tells the decoder how many characters ago the matching sequence was
sent, and the distance indicates the length of the matching sequence. The
size of the distance and length pointers will depend on the size of the
window, for example a window size of 1024 requires the pointers to be 10 bits each.

.. code-block:: c

    %s

In the simulation, a short passage of text is compressed by the encoder
component, sent to the decoder component, decompressed and recovered. A fuller
explanation may be found on `wikipedia <http://en.wikipedia.org/wiki/Lempel%%E2%%80%%93Ziv%%E2%%80%%93Storer%%E2%%80%%93Szymanski>`_.

"""%(indent(open("lzss_compress.c").read()), indent(open("lzss_decompress.c").read()))

    document = open("../docs/source/examples/example_9.rst", "w").write(documentation)

test()
generate_docs()
