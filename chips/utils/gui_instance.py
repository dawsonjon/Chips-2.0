#!/usr/bin/env python

import os
import threading
from math import log

import wx
import wx.aui
import wx.py.editwindow
import wx.stc as stc

from chips.compiler.types import size_of
from chips.compiler.register_map import rregmap, frame
import chips.compiler.profiler as profiler
from chips.compiler.exceptions import StopSim, BreakSim
from chips_c import bits_to_float, bits_to_double
from chips.utils.gui_report import GuiReport

keywords = ["auto", "break", "case", "char", "const", "continue", "default",
            "do", "double", "else", "enum", "extern", "float", "for", "goto",
            "if", "int", "long", "register", "return", "short", "signed",
            "sizeof", "static", "struct", "switch", "typedef", "union",
            "unsigned", "void", "volatile", "while", "input", "output",
            "report", "assert", ]

image_dir = os.path.join(os.path.dirname(__file__), "icons")


class GuiInstance(wx.Frame):

    def __init__(self, parent, instance):
        wx.Frame.__init__(
            self,
            parent,
            title=instance.component_name + " " + str(id(instance)),
            size=(1024,
                  768))
        self.instance = instance
        self.parent = parent

        # tell FrameManager to manage this frame
        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)

        # Status Bar
        self.statusbar = self.CreateStatusBar(4, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-1, -2, -5, -1])

        # Toolbar
        toolbar = wx.ToolBar(
            self,
            -1,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TB_FLAT | wx.TB_NODIVIDER)

        self.reset = toolbar.AddLabelTool(
            wx.NewId(),
            "Reset",
            wx.Bitmap(os.path.join(image_dir, "reset.png")),
            wx.Bitmap(os.path.join(image_dir, "reset_disabled.png")),
            shortHelp="Reset Simulation"
        )
        self.tick = toolbar.AddLabelTool(
            wx.NewId(),
            "Step",
            wx.Bitmap(os.path.join(image_dir, "tick.png")),
            wx.Bitmap(os.path.join(image_dir, "tick_disabled.png")),
            shortHelp="Simulation Step"
        )
        self.into = toolbar.AddLabelTool(
            wx.NewId(),
            "Step Into",
            wx.Bitmap(os.path.join(image_dir, "into.png")),
            wx.Bitmap(os.path.join(image_dir, "into_disabled.png")),
            shortHelp="Step Into"
        )
        self.over = toolbar.AddLabelTool(
            wx.NewId(),
            "Step Over",
            wx.Bitmap(os.path.join(image_dir, "over.png")),
            wx.Bitmap(os.path.join(image_dir, "over_disabled.png")),
            shortHelp="Step Over"
        )
        self.run = toolbar.AddLabelTool(
            wx.NewId(),
            "run",
            wx.Bitmap(os.path.join(image_dir, "run.png")),
            wx.Bitmap(os.path.join(image_dir, "run_disabled.png")),
            shortHelp="Run to breakpoint"
        )
        self.stop = toolbar.AddLabelTool(
            wx.NewId(),
            "stop",
            wx.Bitmap(os.path.join(image_dir, "stop.png")),
            wx.Bitmap(os.path.join(image_dir, "stop_disabled.png")),
            shortHelp="StopSimualtion"
        )
        self.report_memory_usage = toolbar.AddLabelTool(
                wx.NewId(), 
                "report memory usage", 
                wx.Bitmap(os.path.join(image_dir, "stop.png")), 
                wx.Bitmap(os.path.join(image_dir, "stop_disabled.png")), 
                shortHelp="Report Memory Usage"
        )
        self.report_code_coverage = toolbar.AddLabelTool(
                wx.NewId(), 
                "report coverage", 
                wx.Bitmap(os.path.join(image_dir, "stop.png")), 
                wx.Bitmap(os.path.join(image_dir, "stop_disabled.png")), 
                shortHelp="Report Code Coverage"
        )
        self.stop.Enable(False)
        self.Bind(wx.EVT_TOOL, self.on_reset, self.reset)
        self.Bind(wx.EVT_TOOL, self.on_tick, self.tick)
        self.Bind(wx.EVT_TOOL, self.on_over, self.over)
        self.Bind(wx.EVT_TOOL, self.on_into, self.into)
        self.Bind(wx.EVT_TOOL, self.on_run, self.run)
        self.Bind(wx.EVT_TOOL, self.on_stop, self.stop)

        self._mgr.AddPane(toolbar, wx.aui.AuiPaneInfo().
                          Caption("Toolbar").
                          ToolbarPane().
                          Top().
                          LeftDockable(False).
                          RightDockable(False)
                          )

        # code = wx.py.editwindow.EditWindow(self,  -1)
        code = wx.aui.AuiNotebook(self, style=wx.aui.AUI_NB_TOP |
                                  wx.aui.AUI_NB_TAB_SPLIT |
                                  wx.aui.AUI_NB_TAB_MOVE |
                                  wx.aui.AUI_NB_SCROLL_BUTTONS)
        # font1 = wx.Font(12, wx.TELETYPE, wx.NORMAL, wx.NORMAL, False)
        # code.SetFont(font1)

        locals_window = wx.TextCtrl(
            self,
            -1,
            style=wx.TE_MULTILINE | wx.TE_RICH)
        font1 = wx.Font(12, wx.TELETYPE, wx.NORMAL, wx.NORMAL, False)
        locals_window.SetFont(font1)

        globals_window = wx.TextCtrl(
            self,
            -1,
            style=wx.TE_MULTILINE | wx.TE_RICH)
        font1 = wx.Font(12, wx.TELETYPE, wx.NORMAL, wx.NORMAL, False)
        globals_window.SetFont(font1)

        registers_window = wx.TextCtrl(
            self,
            -1,
            style=wx.TE_MULTILINE | wx.TE_RICH)
        font1 = wx.Font(12, wx.TELETYPE, wx.NORMAL, wx.NORMAL, False)
        registers_window.SetFont(font1)

        instructions_window = wx.py.editwindow.EditWindow(self, -1)
        font1 = wx.Font(12, wx.TELETYPE, wx.NORMAL, wx.NORMAL, False)
        instructions_window.SetFont(font1)

        self._mgr.AddPane(code, wx.aui.AuiPaneInfo().
                          Caption("code").
                          CentrePane().
                          CloseButton(False).
                          MinimizeButton(True).
                          BestSize((700, 500))
                          )
        self._mgr.AddPane(registers_window, wx.aui.AuiPaneInfo().
                          Caption("registers").
                          Left().
                          CloseButton(False).
                          MinimizeButton(True).
                          BestSize((700, 500))
                          )
        self._mgr.AddPane(locals_window, wx.aui.AuiPaneInfo().
                          Caption("locals").
                          Left().
                          CloseButton(False).
                          MinimizeButton(True).
                          BestSize((700, 500))
                          )
        self._mgr.AddPane(globals_window, wx.aui.AuiPaneInfo().
                          Caption("globals").Left().
                          CloseButton(False).
                          MinimizeButton(True).
                          BestSize((700, 500))
                          )
        self._mgr.AddPane(instructions_window, wx.aui.AuiPaneInfo().
                          Caption("instructions").
                          Bottom().
                          CloseButton(False).
                          MinimizeButton(True).
                          BestSize((700, 500))
                          )

        self._mgr.Update()

        self.code = code
        self.locals_window = locals_window
        self.registers_window = registers_window
        self.globals_window = globals_window
        self.instructions_window = instructions_window
        self.breakpoints = {}
        self.Bind(wx.EVT_CLOSE, self.on_exit)
        self.open_files()
        self.instance.model.profile=True

        self.Show()

    def open_files(self):
        self.file_windows = {}
        self.file_mapping = {}
        code_files = sorted(
            profiler.code_files(self.instance.model.instructions))
        for i, f in enumerate(code_files):
            # use a keyword argument to force argument to be bound now
            def call_handler(event, ff=f):
                return self.on_set_breakpoint(ff, event)
            cw = wx.py.editwindow.EditWindow(self.code, -1)
            cw.Bind(wx.EVT_LEFT_DCLICK, call_handler)
            #cw.Bind(wx.EVT_RIGHT_DOWN, context_menu)
            self.file_windows[f] = cw
            self.code.AddPage(cw, f)
            ff = open(f, "r")
            cw.AddText(ff.read())
            cw.SetReadOnly(True)
            ff.close()
            cw.setDisplayLineNumbers(True)
            self.file_mapping[f] = i

        display = ""
        for i, instruction in enumerate(self.instance.model.instructions):
            z = instruction.get("z", 0)
            a = instruction.get("a", 0)
            b = instruction.get("b", 0)
            o = instruction.get("op", "unknown")
            literal = instruction.get("literal", 0)
            label = instruction.get("label", 0)
            display += "%0.10d: %s %0.2d %0.2d %0.10d\n" % (
                i, o.ljust(11), z, a, (b | label | literal))
        self.instructions_window.AddText(display)

    def update_code(self, filename, lineno):
        for cw in self.file_windows.values():
            cw.MarkerDeleteAll(0)
        cw = self.file_windows[filename]
        cw.GotoLine(lineno - 1)
        cw.MarkerDefine(0, stc.STC_MARK_ARROW, "blue", "blue")
        cw.MarkerAdd(lineno - 1, 0)
        cw.SetLexerLanguage("cpp")
        cw.SetKeyWords(0, " ".join(keywords))
        cw.Colourise(0, -1)
        self.code.SetSelection(self.file_mapping[filename])


    def mem_location_as_value(self, memory, type_, size, location):

        if size == 4:
            value = memory.get(location, 0)
            if type_ == "int":
                return value
            elif type_ == "float":
                return bits_to_float(value)
        elif size == 8:
            value = memory.get(location, 0) | memory.get(location + 1, 0) << 32
            if type_ == "long":
                return value
            elif type_ == "double":
                return bits_to_double(value)

        return 0

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
            type_ = instance.type_()
            frame_val = registers[frame]
            display += "%s %s %s\n" % (
                type_,
                name,
                self.mem_location_as_value(
                    memory,
                    type_,
                    size,
                    frame_val + offset))
        self.locals_window.SetValue(display)

    def update_registers(self):
        model = self.instance.model
        registers = model.get_registers()
        display = ""
        for number in range(16):
            register = registers.get(number, 0)
            display += "%0.2d: %0.10u %s\n" % (
                number, register, rregmap.get(number, "reserved"))
        self.registers_window.SetValue(display)

    def update_globals(self):
        model = self.instance.model
        instruction = model.get_instruction()
        trace = instruction["trace"]
        global_scope = trace.global_scope
        memory = model.get_memory()

        display = ""
        for name, instance in global_scope.global_variables.iteritems():
            offset = instance.offset
            size = size_of(instance)
            type_ = instance.type_()
            display += "%s %s %s\n" % (
                type_,
                name,
                self.mem_location_as_value(
                    memory,
                    type_,
                    size,
                    offset))

        self.globals_window.SetValue(display)

    def update_instructions(self):
        model = self.instance.model
        lineno = model.get_program_counter()
        self.instructions_window.GotoLine(lineno)
        self.instructions_window.MarkerDefine(
            0, stc.STC_MARK_ARROW, "blue", "blue")
        self.instructions_window.MarkerDeleteAll(0)
        self.instructions_window.MarkerAdd(lineno, 0)

    def update_status(self):
        self.statusbar.SetStatusText("step: " + str(self.parent.chip.time), 0)
        self.statusbar.SetStatusText(
            "memory: " + str(self.instance.model.max_stack),
            1)
        self.statusbar.SetStatusText(
            "file: " + self.instance.model.get_file(),
            2)
        self.statusbar.SetStatusText(
            "line: " + str(self.instance.model.get_line()),
            3)

    def update(self):
        filename = self.instance.model.get_file()
        lineno = self.instance.model.get_line()
        self.update_code(filename, lineno)
        self.update_locals()
        self.update_globals()
        self.update_status()
        self.update_registers()
        self.update_instructions()

    def on_reset(self, arg):
        self.wrap_sim(self.parent.chip.simulation_reset)
        self.parent.update()

    def on_tick(self, arg):
        self.wrap_sim(self.parent.chip.simulation_step)
        self.parent.update()

    def on_over(self, arg):

        def over():
            model = self.instance.model
            s = model.get_instruction()["trace"].statement
            frame_val = model.get_registers().get(frame, 0)
            while (s == model.get_instruction()["trace"].statement
                   or frame_val < model.get_registers().get(frame, 0)):
                if self.wrap_sim(self.parent.chip.simulation_step):
                    break
                if not self.parent.running:
                    break
            self.parent.set_not_running()

        self.run_in_thread(over)

    def on_into(self, arg):

        def into():
            model = self.instance.model
            s = model.get_instruction()["trace"].statement
            while s == model.get_instruction()["trace"].statement:
                if self.wrap_sim(self.parent.chip.simulation_step):
                    break
                if not self.parent.running:
                    break
            self.parent.set_not_running()

        self.run_in_thread(into)

    def on_run(self, arg):

        def run():
            while True:
                if self.wrap_sim(self.parent.chip.simulation_step):
                    break
                if not self.parent.running:
                    break
            self.parent.set_not_running()

        self.run_in_thread(run)

    def on_stop(self, arg):
        self.parent.set_not_running()

    def on_set_breakpoint(self, filename, event):
        cw = event.GetEventObject()
        cw.MarkerDefine(1, stc.STC_MARGIN_SYMBOL, "red", "red")
        lineno = cw.LineFromPosition(
            cw.PositionFromPoint(event.GetPosition())) + 1
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

    def run_in_thread(self, f):
        self.parent.thread = threading.Thread(target=f)
        self.parent.set_running()

    def wrap_sim(self, sim_function):
        """
        Wrap simulations in this function to prevent sim related exceptions
        getting out.
        """
        try:
            sim_function()
        except BreakSim:
            return True
            pass
        except StopSim:
            return True
            pass

    def on_report_code_coverage(self, event):
        report = GuiReport(self, "Code Coverage Report")

        files = self.instance.model.get_profile()
        instructions = self.instance.model.instructions
        for filename in sorted(profiler.code_files(instructions)):
            lines    = files.get(filename, {})
            included = len(profiler.code_lines(filename, instructions))
            executed = len(lines)

            report.report("%s%s%s%s"%(
                filename.ljust(100),
                str(included).center(10),
                str(executed).center(10),
                100.0 * float(executed)/float(included)
            ), float(executed)/float(included))

        total = 0
        for f in sorted(profiler.code_files(instructions)):
            lines = files.get(f, {})
            for lines, count in lines.iteritems():
                total += count

        for filename in sorted(code_files(instructions)):
            lines = files.get(filename, {})
            for line, count in sorted(lines.items(), key=operator.itemgetter(1), reverse=True):
                report.report("%s %s %s" %(
                filename.ljust(100),
                str(line).center(10)))
                print 100.0 * float(count) / float(total)

    def annotate_coverage(self, filename):
        report = GuiReport(self, "Annotated Code Coverage")
        
        files = self.instance.model.get_profile()
        instructions = self.instance.model.instructions
        total = 0.0
        for f in sorted(profiler.code_files(instructions)):
            lines = files.get(f, {})
            for lines, count in lines.iteritems():
                total += count

        source = open(filename)
        included = profiler.code_lines(filename, instructions)
        lines = files.get(filename, {})

        for lineno, line in enumerate(source):
            report_line = str(lineno+1) + " "
            report_line += str(lines.get(lineno+1, 0)).ljust(10) + " "
            if lineno+1 in lines:
                report_line += "> "
                status = log(lines[lineno + 1])/log(total)
            else:
                if lineno+1 in included:
                    report_line += "! "
                    status = 0
                else:
                    report_line += "- "
                    status = 0

            report.report(report_line + line.strip(), status)
