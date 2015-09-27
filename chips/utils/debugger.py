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

from chips.utils.gui_instance import GuiInstance
from chips.utils.gui_report import GuiReport

image_dir = os.path.join(os.path.dirname(__file__), "icons")

class Debugger(wx.Frame):

    def __init__(self, chip):
        app = wx.App()
        wx.Frame.__init__(self, None, title="Chip", size=(1024,768))

        self.chip = chip
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
        self.chip.simulation_reset()
        self.update()
        self.Show()
        self.timer = wx.Timer(self, -1)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.set_not_running()
        app.MainLoop()


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

    def set_running(self):
        self.running=True
        for i in self.instance_windows.values():
            i.reset.Enable(False)
            i.tick.Enable(False)
            i.into.Enable(False)
            i.over.Enable(False)
            i.run.Enable(False)
            i.stop.Enable(True)
        self.timer.Start(1000)
        self.thread.start()

    def set_not_running(self):
        self.running=False
        for i in self.instance_windows.values():
            i.reset.Enable(True)
            i.tick.Enable(True)
            i.into.Enable(True)
            i.over.Enable(True)
            i.run.Enable(True)
            i.stop.Enable(False)

    def on_timer(self, arg):
        if not self.running:
            self.timer.Stop()
        self.update()

    def update(self):
        self.instance_list.Clear()
        for instance in self.chip.instances:
            description = "%s id:%s file:%s line:%s"%(
                    instance.component_name,
                    str(id(instance)),
                    instance.model.get_file(),
                    instance.model.get_line(),
            )
            self.instance_list.Append(description, instance)

        for window in self.instance_windows.values():
            window.update()

    def report_memory_usage(self, event):
        report = GuiReport(self, "memory usage report")
        report.report("memory usage report for %s\n"%self.chip.name, 0)
        report.report("data memory:", 0)
        for instance in self.chip.instances:
            report_line = "%20s : %4u KiB + %4u bytes (%4u 32 bit words)"%(
                instance.component_name,
                (instance.model.max_stack*4) // 1024,
                (instance.model.max_stack*4) % 1024,
                instance.model.max_stack,
            )
            report.report(report_line, 0)

if __name__ == "__main__":
    from chips.components.components import *
    chip = Chip("a chip")
    discard(chip, constant(chip, 0))
    discard(chip, constant(chip, 0))
    discard(chip, constant(chip, 0))
    Debugger(chip)
