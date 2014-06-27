from chips.api.api import *

comp = Component("play.c")
chip = Chip("mychip")

comp(
        chip,
        inputs = {
            "a": Input(chip, "a"),
        },
        outputs = {
        },
        parameters = {
            "START": 10,
            "STOP": 20,
        }
)

comp(
        chip,
        inputs = {
            "a": Input(chip, "b"),
        },
        outputs = {
        },
        parameters = {
            "STOP": 40,
            "START": 30,
        }
)

chip.generate_verilog()
chip.generate_testbench(100000)
chip.compile_iverilog(True)
chip.simulation_reset()
chip.simulation_run()

