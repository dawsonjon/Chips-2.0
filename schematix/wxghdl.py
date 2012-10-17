#!/usr/bin/env python

import wx
import subprocess
import os
import tempfile
import shelve
try:
    import wx
    import wx.lib.agw.floatspin as FS
except:
    print "You need to install wxpython to run this software"
    exit(0)

######################################################################
##USER SETTINGS
######################################################################
editor = "gedit"
new_file_template = """
    --your header here

    library ieee;
    use ieee.std_logic_1164.all;
    use ieee.numeric_std.all;

    entity <entity> is
    begin
    end entity;

    architecture <architecture> of <entity> is
    end architecture;
"""

######################################################################
##END USER SETTINGS
######################################################################

temp_dir=tempfile.mkdtemp()
wave_file=os.path.join(temp_dir, "wave.ghw")
metric_prefix = {
    "fs" : 1e-15,
    "ps" : 1e-12,
    "ns" : 1e-9,
    "us" : 1e-6,
    "ms" : 1e-3,
    "s" : 1
}

def discover_files(root):
    paths = []
    for file_name in os.listdir(root):
        path = os.path.join(root, file_name)
        if path.endswith(".vhd") or path.endswith(".vhdl"):
            paths.append(path)
        elif os.path.isdir(path):
            paths.extend(discover_files(path))
    return paths

class VHDLProject:
    def __init__(self, project_settings):
        self.frame = wx.Frame(None, title = "wxGHDL", size=(1024,600))

        self.project_settings = project_settings

        #create menu bar
        #===============
        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        sim_menu = wx.Menu()
        menubar.Append(file_menu, "File")
        menubar.Append(sim_menu, "Simulation")
        self.frame.SetMenuBar(menubar)

        #File Menu
        #---------
        self.menu_open_project = file_menu.Append(wx.ID_OPEN, "Open", "Open Project")
        self.frame.Bind(wx.EVT_MENU, lambda event:self.load(), self.menu_open_project)

        self.menu_save_project = file_menu.Append(wx.ID_SAVE, "Save", "Save Project")
        self.frame.Bind(wx.EVT_MENU, lambda event:self.save(), self.menu_save_project)

        #Simulation Menu
        #---------------
        self.menu_compile_sim = sim_menu.Append(-1, "Compile", "Compile Simulation")
        self.frame.Bind(wx.EVT_MENU, lambda event:self.compile_simulation(), self.menu_compile_sim)

        self.menu_run_sim = sim_menu.Append(-1, "Run", "Run Simulation")
        self.frame.Bind(wx.EVT_MENU, lambda event:self.run_simulation(), self.menu_run_sim)

        self.menu_view_wave = sim_menu.Append(-1, "View Wave", "Launch GTKWave")
        self.frame.Bind(wx.EVT_MENU, lambda event:self.view_wave(), self.menu_view_wave)

        #create toolbar
        #==============

        #create time settings
        #--------------------
        self.time_control = wx.SpinCtrl(self.frame, -1)
        self.time_control.SetRange(1,999)
        self.time_control.SetValue(1)
        self.time_units_control = wx.ComboBox(self.frame, -1, "us")
        self.time_units_control.Append("fs")
        self.time_units_control.Append("ps")
        self.time_units_control.Append("ns")
        self.time_units_control.Append("us")
        self.time_units_control.Append("ms")
        self.time_units_control.Append("s")

        #create tool bar
        #-------------------
        toolbar = wx.BoxSizer(wx.HORIZONTAL)
        toolbar.Add(wx.StaticText(self.frame, -1, "Run time"), 0, wx.CENTRE)
        toolbar.Add(self.time_control)
        toolbar.Add(self.time_units_control)

        #create file window
        #==================
        self.file_tree = wx.TreeCtrl(self.frame, -1)
        self.file_tree.Bind(wx.EVT_RIGHT_DOWN, self.show_library_menu)

        #create transcript window
        #========================
        self.transcript = wx.TextCtrl(self.frame, -1, style=wx.TE_MULTILINE | wx.TE_RICH2)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(toolbar, 0, wx.EXPAND)
        sizer.Add(self.file_tree, 2, wx.EXPAND)
        sizer.Add(self.transcript, 1, wx.EXPAND)
        self.frame.SetSizer(sizer)
        self.frame.Show()

        self.frame.Bind(wx.EVT_TIMER, self.on_timer)
        self.timer = wx.Timer(self.frame)
        self.process = None
        self.update_state("no_project_open")

    def update_state(self, state):
        self.state = state
        if state == "no_project_open":
            self.menu_save_project.Enable(False)
            self.menu_compile_sim.Enable(False)
            self.menu_run_sim.Enable(False)
            self.menu_view_wave.Enable(False)
        elif state == "project_open":
            self.menu_save_project.Enable(True)
            self.menu_compile_sim.Enable(True)
            self.menu_run_sim.Enable(False)
            self.menu_view_wave.Enable(False)
        elif state == "sim_compiled":
            self.menu_save_project.Enable(True)
            self.menu_compile_sim.Enable(True)
            self.menu_run_sim.Enable(True)
            self.menu_view_wave.Enable(False)
        elif state == "sim_run":
            self.menu_save_project.Enable(True)
            self.menu_compile_sim.Enable(True)
            self.menu_run_sim.Enable(True)
            self.menu_view_wave.Enable(True)

    def show_library_menu(self, event):
        pt = event.GetPosition();
        item, flags = self.file_tree.HitTest(pt)

        if self.file_tree.GetPyData(item) == "root":
            label = self.file_tree.GetItemText(item)
            popupmenu = wx.Menu()
            add_library = popupmenu.Append(-1, "Add a new library")
            self.frame.Bind(wx.EVT_MENU, lambda event: self.new_library(), add_library)
            self.frame.PopupMenu(popupmenu)
        elif self.file_tree.GetPyData(item) == "library":
            library = item
            popupmenu = wx.Menu()
            new_file = popupmenu.Append(-1, "Create a new file")
            self.frame.Bind(wx.EVT_MENU, lambda event: self.new_file(library), new_file)
            add_file = popupmenu.Append(-1, "Add an existing file")
            self.frame.Bind(wx.EVT_MENU, lambda event: self.add_file(library), add_file)
            add_directory = popupmenu.Append(-1, "Add files from directory")
            self.frame.Bind(wx.EVT_MENU, lambda event: self.add_directory(library), add_directory)
            self.frame.PopupMenu(popupmenu)
        elif self.file_tree.GetPyData(item) == "file":
            label = self.file_tree.GetItemText(item)
            filename = label
            file_node = item
            popupmenu = wx.Menu()
            edit_source = popupmenu.Append(-1, "Open in text editor")
            self.frame.Bind(wx.EVT_MENU, lambda event: self.launch_editor(filename), edit_source)
            delete_file = popupmenu.Append(-1, "Delete from library")
            self.frame.Bind(wx.EVT_MENU, lambda event: self.delete_file(file_node), delete_file)
            self.frame.PopupMenu(popupmenu)
     
    def launch_editor(self, filename):
        self.transcript.WriteText("Launching Text Editor\n")
        subprocess.Popen("{0} {1}".format(editor, filename), shell=True)

    def new_library(self):
        dlg = wx.TextEntryDialog(
                self.frame, 
                "Library Name")
        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
            node = self.file_tree.AppendItem(self.root_node, name)
            self.file_tree.SetPyData(node, "library")

    def new_file(self, library):
        dlg = wx.FileDialog(
                self.frame, 
                "Add file", 
                style=wx.SAVE,
                wildcard="VHDL files (*.vhd;*.vhdl)|*.vhd;*.vhdl")
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            new_file = open(filename, "w")
            new_file.write(new_file_template)
            node = self.file_tree.AppendItem(library, filename)
            self.file_tree.SetPyData(node, "file")

    def add_file(self, library):
        dlg = wx.FileDialog(
                self.frame, 
                "Add file", 
                style=wx.OPEN,
                wildcard="VHDL files (*.vhd;*.vhdl)|*.vhd;*.vhdl")
        if dlg.ShowModal() == wx.ID_OK:
            node = self.file_tree.AppendItem(library, dlg.GetPath())
            self.file_tree.SetPyData(node, "file")

    def add_directory(self, library):
        dlg = wx.DirDialog(
                self.frame, 
                "Add directory", 
                style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            paths = discover_files(dlg.GetPath())
            for path in paths:
                node = self.file_tree.AppendItem(library, path)
                self.file_tree.SetPyData(node, "file")

    def delete_file(self, file_node):
        node = self.file_tree.Delete(file_node)

    def compile_simulation(self):
        self.transcript.WriteText("launching GHDL VHDL compiler\n")
        for library, paths in self.project_settings["libraries"].iteritems():
            for path in paths:
                command = 'ghdl -a --work={0} --workdir={1} {2}'.format(
                        library, 
                        temp_dir,
                        path)
                process = subprocess.Popen(
                        command, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.STDOUT, 
                        shell=True)
                for line in process.stdout:
                    self.transcript.WriteText(line)
                process.wait()

        command = 'ghdl -e --work={0} --workdir={1} {2}'.format(
                self.project_settings["top_lib"],
                temp_dir,
                self.project_settings["top_entity"]
                )
        process = subprocess.Popen(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                shell=True)

        for line in process.stdout:
            self.transcript.WriteText(line)
        process.wait()

        if process.returncode == 0:
            self.update_state("sim_compiled")
            self.transcript.WriteText("GHDL VHDL compile ... successful\n")
        else:
            self.update_state("project_open")
            self.transcript.WriteText("GHDL VHDL compile ... failed\n")


    def run_simulation(self):
        self.transcript.WriteText("launching GHDL simulation\n")
        time_to_run = "".join([
            str(self.time_control.GetValue()), 
            self.time_units_control.GetValue()
        ])
        command = "./streams_vhdl_model --wave={0} --stop-time={1}".format(
                wave_file,
                time_to_run
        )
        self.process = subprocess.Popen(command, 
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True)
        self.timer.Start(100)

    def on_timer(self, event):
        try:
            for i in range(100):
                line = next(self.process.stdout)
                self.transcript.WriteText(line)
        except StopIteration:
            self.timer.Stop()
            self.process.wait()
            if self.process.returncode == 0:
                self.update_state("sim_run")
                self.transcript.WriteText("GHDL simulation ... successful\n")
            else:
                self.update_state("sim_compiled")
                self.transcript.WriteText("GHDL simulation ... failed\n")

    def view_wave(self):
        self.transcript.WriteText("launching GTKWave waveform viewer\n")
        subprocess.Popen("gtkwave {0}".format(wave_file), shell=True)
        

    def project_to_window(self):
        self.file_tree.DeleteAllItems()
        self.root_node = self.file_tree.AddRoot("Libraries")
        self.file_tree.SetPyData(self.root_node, "root")

        for library, paths in self.project_settings["libraries"].iteritems():
            library_node = self.file_tree.AppendItem(self.root_node, library)
            self.file_tree.SetPyData(library_node, "library")
            for path in paths:
                node = self.file_tree.AppendItem(library_node, path)
                self.file_tree.SetPyData(node, "file")

        self.file_tree.ExpandAll()

if __name__ == "__main__":
    app = wx.App()
    VHDLProject()
    app.MainLoop()
