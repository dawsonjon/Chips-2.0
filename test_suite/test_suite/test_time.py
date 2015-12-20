from chips.api.api import *

chip = Chip("test")

response = Response(chip, "blah", "int")

test_time = Component("test_time.c")
test_time(chip,
        inputs = { },
        outputs = {"console":response},
)

chip.simulation_reset()
chip.simulation_run()
print "".join([chr(i) for i in response])
