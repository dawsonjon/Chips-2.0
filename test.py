from chips.api.api import *
import sys

try:

    my_chip = Chip("my_chip")

    a = Input(my_chip, "a")
    b = Input(my_chip, "b")
    z = Output(my_chip, "z")

    Component("adder.c")(my_chip, inputs={"a":a, "b":b}, outputs={"z":z})

    my_chip.generate_verilog()
    my_chip.generate_testbench()

except C2CHIPError as err:
    print "Error in file:", err.filename, "at line:", err.lineno
    print err.message
    sys.exit(-1)
