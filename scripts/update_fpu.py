#!/usr/bin/env python
import os.path

divider = open(os.path.join("fpu", "divider", "divider.v")).read()
multiplier = open(os.path.join("fpu", "multiplier", "multiplier.v")).read()
adder = open(os.path.join("fpu", "adder", "adder.v")).read()
output_file = open(os.path.join("chips", "compiler", "fpu.py"), "w")

output_file.write("divider = \"\"\"%s\"\"\"\n"%divider)
output_file.write("multiplier = \"\"\"%s\"\"\"\n"%multiplier)
output_file.write("adder = \"\"\"%s\"\"\"\n"%adder)
