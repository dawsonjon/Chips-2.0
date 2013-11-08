from chips.api.api import *
import sys

try:

    my_chip = Chip("my_chip")

    a = Wire(my_chip)
    b = Wire(my_chip)
    z = Wire(my_chip)

    stim = Component("stimulus.c")
    stim(my_chip, inputs=[], outputs=[a])
    stim(my_chip, inputs=[], outputs=[b])
    Component("adder.c")(my_chip, inputs=[a, b], outputs=[z])
    response = Component("response.c")
    response(my_chip, inputs=[z], outputs=[])

    my_chip.generate_verilog()

except C2CHIPError as err:
    print "Error in file:", err.filename, "at line:", err.lineno
    print err.message
    sys.exit(-1)
