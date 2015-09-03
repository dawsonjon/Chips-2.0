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

my_chip = Chip("interconnect")
wire = Wire(my_chip)
Component("test_suite/float_producer.c")(my_chip, inputs={}, outputs={"z":wire})
Component("test_suite/float_consumer.c")(my_chip, inputs={"a":wire}, outputs={})
my_chip.simulation_reset()
my_chip.simulation_run()

my_chip = Chip("interconnect")
wire = Wire(my_chip)
Component("test_suite/double_producer.c")(my_chip, inputs={}, outputs={"z":wire})
Component("test_suite/double_consumer.c")(my_chip, inputs={"a":wire}, outputs={})
my_chip.simulation_reset()
my_chip.simulation_run()

my_chip = Chip("interconnect")
wire = Wire(my_chip)
Component("test_suite/long_producer.c")(my_chip, inputs={}, outputs={"z":wire})
Component("test_suite/long_consumer.c")(my_chip, inputs={"a":wire}, outputs={})
my_chip.simulation_reset()
my_chip.simulation_run()
