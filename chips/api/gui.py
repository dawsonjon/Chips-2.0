#!/usr/bin/env python

import sys
import os
import wx
import wx.aui
import wx.py.editwindow
from wx.lib.splitter import MultiSplitterWindow
import wx.stc as stc

from chips.api.api import Chip
from chips.compiler.types import size_of
from chips.compiler.register_map import rregmap, frame, tos
import chips.compiler.profiler as profiler

from chips.api.breakpoint_dialog import BreakPointDialog
from chips.api.gui_instance import GuiInstance

image_dir = os.path.join(os.path.dirname(__file__), "icons")

class GuiChip(wx.Frame, Chip):

    def debug(self):
        app = wx.App()
        wx.Frame.__init__(self, None, title="Chip", size=(1024,768))

        #create toolbar
        toolbar = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        self.reset = toolbar.AddLabelTool(
                wx.NewId(), 
                "Reset", 
                wx.Bitmap(os.path.join(image_dir, "reset.png")), 
                shortHelp="Reset Simulation"
        )
        self.tick = toolbar.AddLabelTool(
                wx.NewId(), 
                "Step", 
                wx.Bitmap(os.path.join(image_dir, "tick.png")), 
                shortHelp="Machine Instruction Step"
        )
        self.run = toolbar.AddLabelTool(
                wx.NewId(), 
                "run", 
                wx.Bitmap(os.path.join(image_dir, "run.png")), 
                shortHelp="Run to breakpoint"
        )

        self.Bind(wx.EVT_TOOL, self.on_reset, self.reset)
        self.Bind(wx.EVT_TOOL, self.on_tick, self.tick)
        self.Bind(wx.EVT_TOOL, self.on_run,  self.run)


        panel = wx.Panel(self, -1)
        vsizer = wx.BoxSizer(wx.VERTICAL)

        instance_list = wx.ListBox(self, 60, (100, 50), (90, 120), [], wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.on_select_instance, instance_list)

        vsizer.Add(instance_list, 1, wx.EXPAND)
        panel.SetSizer(vsizer)
        sizer=wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        panel.Layout()
        self.Layout()

        self.instance_list = instance_list
        self.instance_windows = {}

        self.Show()
        self.on_reset(None)
        app.MainLoop()

    def __init__(self, *args, **vargs):
        Chip.__init__(self, *args, **vargs)

    def on_reset(self, arg):
        self.simulation_reset()
        self.update()

    def on_tick(self, arg):
        self.simulation_step()
        self.update()

    def on_run(self, arg):
        self.simulation_run()
        self.update()

    def on_select_instance(self, arg):
        selection = self.instance_list.GetSelection()
        instance = self.instance_list.GetClientData(selection)
        idi = id(instance)
        if idi in self.instance_windows:
          window = self.instance_windows[idi]
        else:
          window = GuiInstance(self, instance)
          self.instance_windows[idi]=window

        window.update()
        window.Raise()

    def update(self):
        self.instance_list.Clear()
        for instance in self.instances:
            description = "%s id:%s file:%s line:%s"%(
                    instance.component_name,
                    str(id(instance)),
                    instance.model.get_file(),
                    instance.model.get_line(),
            )
            self.instance_list.Append(description, instance)

        for window in self.instance_windows.values():
            window.update()
