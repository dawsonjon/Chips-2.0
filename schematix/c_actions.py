import os
import editor

def edit(component):

    """Edit a C file"""

    editor.open_file(get_source_path(window, component))
    window.update()

def _import(component):

    """Import an existing C file"""

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
        new_file = name + ".vhd"
        new_file = os.path.join(
            window.project_path.GetValue(),
            new_file)
        new_file = open(new_file, "w")
        new_file.write("--name : %s\n"%name)
        new_file.write("--source_file : %s\n"%(name+".c"))
        new_file.close()
        new_file = name + ".c"
        new_file = os.path.join(
            window.project_path.GetValue(),
            new_file)
        new_file = open(new_file, "w")
        new_file.close()
        window.update()

def generate(window, filename):

    """Make a VHDL component from a C component"""

    os.system("c2vhdl %s")
    window.update()
