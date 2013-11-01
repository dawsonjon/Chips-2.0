#!/usr/bin/env python

import sys
import os
import shutil

from user_settings import xilinx

current_directory = os.getcwd()
working_directory = "synthesis"
shutil.copyfile("xilinx_input/SP605.ucf", os.path.join(working_directory, "SP605.ucf"))
shutil.copyfile("xilinx_input/SP605.prj", os.path.join(working_directory, "SP605.prj"))
os.chdir(working_directory)

if "compile" in sys.argv or "all" in sys.argv:
    retval = os.system("../../../c2verilog ../source/user_design.c")
    retval = os.system("../../../c2verilog ../source/server.c")
    if retval != 0:
        sys.exit(-1)

if "build" in sys.argv or "all" in sys.argv:
    retval = os.system("%s/xflow -synth xst_mixed.opt -p XC6Slx45t-fgg484 -implement balanced.opt -config bitgen.opt SP605"%xilinx)
    if retval != 0:
        sys.exit(-1)

if "download" in sys.argv or "all" in sys.argv:
    command_file = open("download.cmd", 'w')
    command_file.write("setmode -bscan\n")
    command_file.write("setCable -p auto\n")
    command_file.write("identify\n")
    command_file.write("assignfile -p 2 -file SP605.bit\n")
    command_file.write("program -p 2\n")
    command_file.write("quit\n")
    command_file.close()
    retval = os.system("%s/impact -batch download.cmd"%xilinx)
    if retval != 0:
        sys.exit(-1)

os.chdir(current_directory)
