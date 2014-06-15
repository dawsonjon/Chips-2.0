#!/usr/bin/env python

from chips.api.api import *
import sys


my_chip = Chip("interconnect")
wire = Wire(my_chip)
Component("test_suite/producer.c")(my_chip, inputs={}, outputs={"z":wire})
Component("test_suite/consumer.c")(my_chip, inputs={"a":wire}, outputs={})
my_chip.simulation_reset()
my_chip.simulation_run()

my_chip = Chip("interconnect")
wire = Wire(my_chip)
Component("test_suite/slow_producer.c")(my_chip, inputs={}, outputs={"z":wire})
Component("test_suite/consumer.c")(my_chip, inputs={"a":wire}, outputs={})
my_chip.simulation_reset()
my_chip.simulation_run()

my_chip = Chip("interconnect")
wire = Wire(my_chip)
Component("test_suite/producer.c")(my_chip, inputs={}, outputs={"z":wire})
Component("test_suite/slow_consumer.c")(my_chip, inputs={"a":wire}, outputs={})
my_chip.simulation_reset()
my_chip.simulation_run()

my_chip = Chip("interconnect")
wire = Wire(my_chip)
Component("test_suite/slow_producer.c")(my_chip, inputs={}, outputs={"z":wire})
Component("test_suite/slow_consumer.c")(my_chip, inputs={"a":wire}, outputs={})
my_chip.simulation_reset()
my_chip.simulation_run()

os.remove("producer.v")
os.remove("consumer.v")
