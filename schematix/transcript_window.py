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

import editor

class TranscriptWindow(wx.TextCtrl):

    def __init__(self, parent):
        wx.TextCtrl.__init__(self, parent, style=wx.TE_MULTILINE | wx.TE_RICH)
        self.SetEditable(False)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.links = []

    def get_lineno(self):
        return len(self.GetValue().splitlines())-1

    def log(self, message):
        for line in message.strip().splitlines():
            if line.endswith("compilation error"):
                try:
                    filename, lineno, col, rest = self.last_line.split(":")
                    self.link_line(line, filename, lineno)
                except ValueError:
                    pass
            else:
                self.log_line(line)
            self.last_line = line

    def log_line(self, message):
        self.SetDefaultStyle(wx.TextAttr("blue"))
        self.AppendText(message + "\n")

    def link_line(self, message, filename, lineno):
        self.SetDefaultStyle(wx.TextAttr("red"))
        self.AppendText(message + "\n")
        self.links.append((self.get_lineno(), filename, lineno))

    def on_left_down(self, event):
        pt = event.GetPosition();
        result, col, row = self.HitTest(pt)
        for link_row, filename, lineno in self.links:
            if row == link_row:
                editor.open_file(filename, lineno)
                break
        

if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None, -1, "Test")
    window = TranscriptWindow(frame)
    window.log_line("blah\n")
    window.link_line("blah\n")
    window.log_line("blah\n")
    frame.Show()
    app.MainLoop()
