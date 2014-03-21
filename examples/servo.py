#!/usr/bin/env python

from chips.api.api import *
import sys


servo = Chip("servo")
rs232_in = Input(servo, "rs232_in")
rs232_out = Output(servo, "rs232_out")
servos = Output(servo, "servos")
control = Wire(servo)

ui = Component("servo_ui.c")
ui(
    servo, 
    inputs={
        "rs232":rs232_in,
    }, 
    outputs={
        "rs232":rs232_out,
        "control":control,
    }
)

controller = Component("servo_controller.c")

controller(
    servo, 
    inputs={
        "control":control,
    }, 
    outputs={
        "servos":servos,
    },
)

servo.generate_verilog()
servo.generate_testbench(100000)
servo.compile_iverilog(True)

