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

keywords = ["auto", "break", "case", "char", "const", "continue", "default",
"do", "double", "else", "enum", "extern", "float", "for", "goto", "if", "int",
"long", "register", "return", "short", "signed", "sizeof", "static", "struct",
"switch", "typedef", "union", "unsigned", "void", "volatile", "while", "input", 
"output", "report", "assert",
]

image_dir = os.path.join(os.path.dirname(__file__), "icons")

class GuiInstance(wx.Frame):

    def __init__(self, parent, instance):
        wx.Frame.__init__(self, parent, title=instance.component_name + " " + str(id(instance)), size=(1024,768))
        self.instance = instance
        self.parent = parent

        # tell FrameManager to manage this frame        
        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)

        #Status Bar
        self.statusbar = self.CreateStatusBar(3, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-1, -5, -1])

        #Toolbar
        toolbar = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize, wx.TB_FLAT | wx.TB_NODIVIDER)

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
                shortHelp="Simulation Step"
        )
        self.into = toolbar.AddLabelTool(
                wx.NewId(), 
                "Step Into", 
                wx.Bitmap(os.path.join(image_dir, "into.png")), 
                shortHelp="Step Into"
        )
        self.over = toolbar.AddLabelTool(
                wx.NewId(), 
                "Step Over", 
                wx.Bitmap(os.path.join(image_dir, "over.png")), 
                shortHelp="Step Over"
        )
        self.run = toolbar.AddLabelTool(
                wx.NewId(), 
                "run", 
                wx.Bitmap(os.path.join(image_dir, "run.png")), 
                shortHelp="Run to breakpoint"
        )
        self.Bind(wx.EVT_TOOL, self.on_reset, self.reset)
        self.Bind(wx.EVT_TOOL, self.on_tick, self.tick)
        self.Bind(wx.EVT_TOOL, self.on_over, self.over)
        self.Bind(wx.EVT_TOOL, self.on_into, self.into)
        self.Bind(wx.EVT_TOOL, self.on_run,  self.run)

        self._mgr.AddPane(toolbar, wx.aui.AuiPaneInfo().
            Caption("Toolbar").
            ToolbarPane().
            Top().
            LeftDockable(False).
            RightDockable(False)
        )

        #code = wx.py.editwindow.EditWindow(self,  -1)
        code = wx.aui.AuiNotebook(self, style = wx.aui.AUI_NB_TOP | 
                                                   wx.aui.AUI_NB_TAB_SPLIT | 
                                                   wx.aui.AUI_NB_TAB_MOVE | 
                                                   wx.aui.AUI_NB_SCROLL_BUTTONS ) 
        #font1 = wx.Font(12, wx.TELETYPE, wx.NORMAL, wx.NORMAL, False)
        #code.SetFont(font1)

        locals_window = wx.TextCtrl(self,  -1, style=wx.TE_MULTILINE|wx.TE_RICH)
        font1 = wx.Font(12, wx.TELETYPE, wx.NORMAL, wx.NORMAL, False)
        locals_window.SetFont(font1)

        globals_window = wx.TextCtrl(self,  -1, style=wx.TE_MULTILINE|wx.TE_RICH)
        font1 = wx.Font(12, wx.TELETYPE, wx.NORMAL, wx.NORMAL, False)
        globals_window.SetFont(font1)

        instructions_window = wx.TextCtrl(self,  -1, style=wx.TE_MULTILINE|wx.TE_RICH)
        font1 = wx.Font(12, wx.TELETYPE, wx.NORMAL, wx.NORMAL, False)
        instructions_window.SetFont(font1)

        self._mgr.AddPane(code, wx.aui.AuiPaneInfo().
                Caption("code").
                CentrePane().
                CloseButton(False).
                MinimizeButton(True).
                BestSize((500, 500))
        )
        self._mgr.AddPane(locals_window, wx.aui.AuiPaneInfo().
                Caption("locals").
                Left().
                CloseButton(False).
                MinimizeButton(True).
                BestSize((500, 500))
        )
        self._mgr.AddPane(globals_window, wx.aui.AuiPaneInfo().
                Caption("globals").Left().
                CloseButton(False).
                MinimizeButton(True).
                BestSize((500, 500))
        )
        self._mgr.AddPane(instructions_window, wx.aui.AuiPaneInfo().
                Caption("instructions").
                Bottom().
                CloseButton(False).
                MinimizeButton(True).
                BestSize((500, 500))
        )

        self._mgr.Update()

        self.code = code
        self.locals_window = locals_window
        self.globals_window = globals_window
        self.breakpoints = {}

        self.open_files()

        self.Show()

    def open_files(self):
        self.file_windows = {}
        self.file_mapping = {}
        code_files = sorted(profiler.code_files(self.instance.model.instructions))
        for i, f in enumerate(code_files):
            #use a keyword argument to force argument to be bound now
            def call_handler(event, ff = f):
                return self.on_set_breakpoint(ff, event)
            cw = wx.py.editwindow.EditWindow(self.code,  -1)
            cw.Bind(wx.EVT_LEFT_DCLICK, call_handler)
            self.file_windows[f] = cw
            self.code.AddPage(cw, f)
            ff = open(f, "r")
            cw.AddText(ff.read())
            ff.close()
            cw.setDisplayLineNumbers(True)
            self.file_mapping[f] = i

    def update_code(self, filename, lineno):
        for cw in self.file_windows.values():
            cw.MarkerDeleteAll(0)
        cw = self.file_windows[filename]
        cw.GotoLine(lineno-1)
        cw.MarkerDefine(0, stc.STC_MARK_ARROW, "blue", "blue")
        cw.MarkerAdd(lineno-1, 0)
        cw.SetLexerLanguage("cpp")
        cw.SetKeyWords(0, " ".join(keywords))
        cw.Colourise(0, -1)
        self.code.SetSelection(self.file_mapping[filename])

    def update_locals(self):
        model = self.instance.model
        instruction = model.get_instruction()
        trace = instruction["trace"]
        function = trace.function
        registers = model.get_registers()
        memory = model.get_memory()
        variables = function.local_variables

        display = ""
        for name, instance in variables.iteritems():
          offset = instance.offset
          size = size_of(instance)
 
          if size == 4:
              display = "%s : %s"%(name, memory.get(tos+offset, 0))
          elif size == 8:
              display = "%s : %s"%(name, memory.get(tos+offset+1, 0) << 32 | memory.get(tos+offset, 0))
          else:
              display = "%s : "%name
              for i in range((size//4)//8):
                  display += "%4x:"%(i*8),
                  for j in range(8):
                      display += "%08x"%memory.get(tos+offset+8*i+j, 0) 
                  display += "\n"
        self.locals_window.SetValue(display)

    def update_globals(self):
        model = self.instance.model
        instruction = model.get_instruction()
        trace = instruction["trace"]
        global_scope = trace.global_scope
        registers = model.get_registers()
        memory = model.get_memory()

        display = ""
        for name, instance in global_scope.global_variables.iteritems():
          offset = instance.offset
          size = size_of(instance)
 
          if size == 4:
              display = "%s : %s"%(name, memory.get(offset, 0))
          elif size == 8:
              display = "%s : %s"%(name, memory.get(offset+1, 0) << 32 | memory.get(offset, 0))
          else:
              display = "%s : "%name
              for i in range((size//4)//8):
                  display += "%4x:"%(i*8),
                  for j in range(8):
                      display += "%08x"%memory.get(offset+8*i+j, 0) 
                  display += "\n"
        self.globals_window.SetValue(display)

    def update_status(self):
        self.statusbar.SetStatusText("step: " + str(self.parent.time), 0)
        self.statusbar.SetStatusText("file: " + self.instance.model.get_file(), 1)
        self.statusbar.SetStatusText("line: " + str(self.instance.model.get_line()), 2)

    def update(self):
        filename=self.instance.model.get_file()
        lineno=self.instance.model.get_line()
        self.update_code(filename, lineno)
        self.update_locals()
        self.update_globals()
        self.update_status()

    def on_reset(self, arg):
        self.parent.simulation_reset()
        self.parent.update()

    def on_tick(self, arg):
        self.parent.simulation_step()
        self.parent.update()

    def on_over(self, arg):
        model = self.instance.model
        l = model.get_line()
        f = model.get_file()
        while(model.get_line() <= l and model.get_file != f):
            self.parent.simulation_step()
        self.parent.update()

    def on_into(self, arg):
        model = self.instance.model
        l = model.get_line()
        f = model.get_file()
        while(l == model.get_line() and f == model.get_file()):
            self.parent.simulation_step()
        self.parent.update()

    def on_run(self, arg):
        self.parent.simulation_run()
        self.parent.update()

    def on_set_breakpoint(self, filename, event):
        cw = event.GetEventObject()
        cw.MarkerDefine(1, stc.STC_MARGIN_SYMBOL, "red", "red")
        lineno = cw.LineFromPosition(cw.PositionFromPoint(event.GetPosition())) + 1
        lines = self.breakpoints.get(filename, {})
        if lineno in lines:
            lines.pop(lineno)
            cw.MarkerDelete(lineno - 1, 1)
            self.instance.model.clear_breakpoint(filename, lineno)
        else:
            self.instance.model.set_breakpoint(filename, lineno)
            lines[lineno] = True
            cw.MarkerAdd(lineno - 1, 1)
        self.breakpoints[filename] = lines

    def on_exit(self, event):
        self.parent.instance_windows.pop(id(self.instance))
        event.Skip()

#      clear()
#      try:
#          #print list of files
#          print "Code Files:"
#          code_files = sorted(profiler.code_files(model.instructions))
#          for i, f in enumerate(code_files):
#              print "[%u] %s"%(i, f)
#
#          #get user selection
#          print "\nEnter file:"
#          selection = raw_input()
#          f = code_files[int(selection)]
#
#          line = 0
#          while 1:
#              clear()
#              print_file_line(f, line)
#              print 
#              print "n=next, p=prev, j=down, k=up, blank=enter"
#              command = raw_input()
#              if command == "n":
#                  line = abs(line + 10)
#              elif command == "n":
#                  line = abs(line - 10)
#              elif command == "j":
#                  line = abs(line + 1)
#              elif command == "k":
#                  line = abs(line - 1)
#              elif command == "":
#                  break
#
#          model.set_breakpoint(f, line)
