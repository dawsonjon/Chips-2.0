import os

import wx

import editor
from chips.compiler.parser import Parser
from chips.compiler.exceptions import C2CHIPError
from chips.compiler.optimizer import parallelise
from chips.compiler.tokens import Tokens
from chips.compiler.verilog import generate_CHIP

def edit(window, component):

    """Edit a C file"""

    editor.open_file(window.get_source_path(component))
    window.transcript.log("Editing C source File")
    window.update()

def _import(window, component):

    """Import an existing C file"""

    window.transcript.log("Importing C source File")
    editor.open_file(component["source_file"])
    window.update()

def new(window):

    """Make a new C file"""

    dlg = wx.TextEntryDialog(
        window, 
        "Component name:",
        "New C File")

    if dlg.ShowModal() == wx.ID_OK:
        name = dlg.GetValue()
        window.transcript.log("Creating Empty C Source File")
        new_file = name + ".c"
        new_file = os.path.join(
            window.project_path.GetValue(),
            new_file)
        new_file = open(new_file, "w")
        new_file.write("int %s()\n"%name)
        new_file.write("{\n")
        new_file.write("  return 0;\n")
        new_file.write("}\n")
        new_file.close()
        window.transcript.log("Creating Empty Component")
        new_file = name + ".v"
        new_file = os.path.join(
            window.project_path.GetValue(),
            new_file)
        new_file = open(new_file, "w")
        new_file.write("//name : %s\n"%name)
        new_file.write("//source_file : %s\n"%(name+".c"))
        new_file.close()
        window.update()

def generate(window, component):

    """Make a verilog component from a C component"""

    window.transcript.log("Compiling C Source File")
    filename = window.get_source_path(component)
    try:
        #compile into CHIP
        parser = Parser(filename, True)
        process = parser.parse_process()
        name = process.main.name
        instructions = process.generate()
        frames = parallelise(instructions)
        output_file = name + ".v"
        output_file = os.path.join(
            window.project_path.GetValue(),
            output_file)
        output_file = open(output_file, "w")
        generate_CHIP(
                filename, 
                name, 
                frames, 
                output_file, 
                parser.allocator.all_registers,
                parser.allocator.memory_size)
        output_file.close()
    except C2CHIPError as err:
      window.transcript.log(err.message)
      window.transcript.link_line("Error in file: %s at line: %s"%(err.filename, err.lineno), 
        err.filename, 
        err.lineno)
      window.update()
