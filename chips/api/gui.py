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

from chips.api.gui_instance import GuiInstance

image_dir = os.path.join(os.path.dirname(__file__), "icons")

class GuiChip(wx.Frame, Chip):

    def debug(self):
        app = wx.App()
        wx.Frame.__init__(self, None, title="Chip", size=(1024,768))

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
        self.simulation_reset()
        self.update()
        self.Show()
        app.MainLoop()

    def __init__(self, *args, **vargs):
        Chip.__init__(self, *args, **vargs)

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
