#!/usr/bin/env python
from chips.api.api import *
from math import ceil, log

try:
    from PIL import Image
except ImportError:
    print "You need Python Imaging Library to run this script!"
    exit(0)

def test():

    test_data = """IN the year 1878 I took my degree of Doctor of Medicine of the
    University of London, and proceeded to Netley to go through the course
    prescribed for surgeons in the army. Having completed my studies there,
    I was duly attached to the Fifth Northumberland Fusiliers as Assistant
    Surgeon. The regiment was stationed in India at the time, and before
    I could join it, the second Afghan war had broken out. On landing at
    Bombay, I learned that my corps had advanced through the passes, and
    was already deep in the enemy's country. I followed, however, with many
    other officers who were in the same situation as myself, and succeeded
    in reaching Candahar in safety, where I found my regiment, and at once
    entered upon my new duties.

    The campaign brought honours and promotion to many, but for me it had
    nothing but misfortune and disaster. I was removed from my brigade and
    attached to the Berkshires, with whom I served at the fatal battle of
    Maiwand. There I was struck on the shoulder by a Jezail bullet, which
    shattered the bone and grazed the subclavian artery. I should have
    fallen into the hands of the murderous Ghazis had it not been for the
    devotion and courage shown by Murray, my orderly, who threw me across a
    pack-horse, and succeeded in bringing me safely to the British lines.
    """

    chip = Chip("compression_test")
    test_in = Stimulus(chip, "test_in", "int", map(ord, test_data))
    wire = Wire(chip)
    test_out = Response(chip, "test_out", "int", 1024)
    
    #create a filter component using the C code
    compressor = Component("lzss_compress.c")
    decompressor = Component("lzss_decompress.c")

    #add an instance to the chip
    compressor(
        chip, 
        inputs = {
            "raw_in":test_in,
        },
        outputs = {
            "compressed_out":wire,
        },
        parameters = {
            "N":1024,
            "LOG2N":ceil(log(1024, 2)),
        },
    )

    #add an instance to the chip
    decompressor(
        chip, 
        inputs = {
            "compressed_in":wire,
        },
        outputs = {
            "raw_out":test_out,
        },
        parameters = {
            "N":1024,
            "LOG2N":ceil(log(1024, 2)),
        },
    )

    #run the simulation
    chip.simulation_reset()
    chip.simulation_run()


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
