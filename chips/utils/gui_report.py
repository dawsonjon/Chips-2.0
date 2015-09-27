#!/usr/bin/env python

import sys
import os
import threading

import wx
import wx.aui
import wx.py.editwindow
from wx.lib.splitter import MultiSplitterWindow
import wx.stc as stc

from chips.api.api import Chip
from chips.compiler.types import size_of
from chips.compiler.register_map import rregmap, frame, tos
import chips.compiler.profiler as profiler
from chips.compiler.exceptions import StopSim, BreakSim
from chips.compiler.utils import bits_to_float, bits_to_double

class GuiReport(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1024,768))
        self.parent = parent

        panel = wx.Panel(self, -1)
        vsizer = wx.BoxSizer(wx.VERTICAL)

        report_window = wx.TextCtrl(panel,  -1, style=wx.TE_MULTILINE|wx.TE_RICH)
        font1 = wx.Font(12, wx.TELETYPE, wx.NORMAL, wx.NORMAL, False)
        report_window.SetFont(font1)
        report_window.SetEditable(False)
        self.report_window = report_window

        vsizer.Add(report_window, 1, wx.EXPAND)
        panel.SetSizer(vsizer)

        sizer=wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)

        panel.Layout()
        self.Layout()
        self.Show()

    def report(self, text, highlight):
        self.report_window.SetDefaultStyle(wx.TextAttr(wx.BLACK, (255, 255 - highlight * 255, 255)))
        self.report_window.AppendText(text + "\n")


if __name__ == "__main__":
        app = wx.App()
        g = GuiReport(None, "profile")
        g.report("blah", 0.5)
        g.report("blah blah", 1)
        
        app.MainLoop()
