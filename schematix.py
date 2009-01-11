#!/usr/bin/env python
import pickle
import copy

import wx
from wx.lib.floatcanvas import NavCanvas, FloatCanvas, Resources
from wx.lib.scrolledpanel import ScrolledPanel

import components
import generator

class BlockFrame(wx.Frame):

    """The main schematic window.

    This class is also responsible for drawing the schematic,
    capturing schematic events, and managing the document objects

    """

    def __init__(self, *args, **kwargs):

        """Create the main Window, and all the associated widgets.

        Initialises to an empty document, and sets up event bindings for 
        widgets."""

        #draw windows
        wx.Frame.__init__(self, *args, **kwargs)

        #make canvas
        canvas = NavCanvas.NavCanvas(self, style=wx.SUNKEN_BORDER)
        self.canvas = canvas.Canvas

        #make menu
        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        self.Bind(wx.EVT_MENU, 
             lambda evt: self.on_open(),
             file_menu.Append(wx.ID_OPEN, "Open"),
        )
        self.Bind(wx.EVT_MENU, 
             lambda evt: self.on_save(),
             file_menu.Append(wx.ID_SAVE, "Save"),
        )
        self.Bind(wx.EVT_MENU, 
             lambda evt: self.on_save_as(),
             file_menu.Append(wx.ID_SAVEAS, "Save As"),
        )
        self.Bind(wx.EVT_MENU, 
             lambda evt: self.on_exit(),
             file_menu.Append(wx.ID_EXIT, "Exit"),
        )
        edit_menu = wx.Menu()

        self.undo = edit_menu.Append(wx.ID_UNDO, "Undo")
        self.redo = edit_menu.Append(wx.ID_REDO, "Redo")

        self.undo.Enable(False)
        self.redo.Enable(False)

        self.Bind(wx.EVT_MENU, lambda evt: self.on_undo(), self.undo)
        self.Bind(wx.EVT_MENU, lambda evt: self.on_redo(), self.redo)

        menubar.Append(file_menu, "File")
        menubar.Append(edit_menu, "Edit")
        self.SetMenuBar(menubar)

        #make component selector
        selector = wx.TreeCtrl(self, style=wx.SUNKEN_BORDER|wx.TR_DEFAULT_STYLE)
        root = selector.AddRoot("items")
        for library_name, library in components.components:
            library_node = selector.AppendItem(root, library_name)
            for component in library:
                title = component["name"]
                node = selector.AppendItem(library_node, title)
                selector.SetItemPyData(node, component)
        self.selector = selector

        #layout windows
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(selector, 1, wx.EXPAND)
        sizer.Add(canvas, 5, wx.EXPAND)
        self.SetSizer(sizer)

        #bind events
        self.state = "idle"
        self.canvas.Bind(FloatCanvas.EVT_LEFT_UP, self.on_left_up)
        self.canvas.Bind(FloatCanvas.EVT_LEFT_DOWN, self.on_left_down)
        self.canvas.Bind(FloatCanvas.EVT_RIGHT_DOWN, self.on_right_down)
        self.canvas.Bind(FloatCanvas.EVT_MOTION, self.on_motion)

        #state that doesn't get saved
        self.undos = []
        self.redos = []

        #state that gets saved
        self.sn = 0
        self.netlist = {}
        self.port_positions = {}
        self.wires = []

    def on_open(self):

        """Open a document"""

        dlg = wx.FileDialog(self, "Open Schematic", style = wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            filename =  dlg.GetPath()
            self.filename = filename
            open_file = open(filename, 'r')
            self.sn = pickle.load(open_file)
            self.netlist = pickle.load(open_file)
            self.port_positions = pickle.load(open_file)
            self.wires = pickle.load(open_file)
            self.draw()
            self.undo.Enable(False)
            self.redo.Enable(False)
            self.undos = []
            self.redos = []

    def on_save_as(self):

        """Save document with a new file name"""

        dlg = wx.FileDialog(self, "Save Schematic", style = wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            save_file = open(self.filename, 'w')
            pickle.dump(self.sn, save_file)
            pickle.dump(self.netlist, save_file)
            pickle.dump(self.port_positions, save_file)
            pickle.dump(self.wires, save_file)

    def on_save(self):

        """Save, prompt for new file name if not allready saved"""

        if not hasattr(self, "filename"):
            dlg = wx.FileDialog(self, "Save Schematic", style = wx.FD_SAVE)
            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetPath()
                save_file = open(self.filename, 'w')
                pickle.dump(self.sn, save_file)
                pickle.dump(self.netlist, save_file)
                pickle.dump(self.port_positions, save_file)
                pickle.dump(self.wires, save_file)

    def export(self):

        """Export to a chips file"""

        dlg = wx.FileDialog(self, "Export", style = wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            generator.generate(
                filename,
                self.netlist, 
                self.port_positions, 
                self.wires
            )


    def snapshot(self):

        """This gets called before anything significant changes.
        
        The state of the document is placed on a stack so that changes 
        can be undone"""

        stuff = self.sn, self.netlist, self.port_positions, self.wires
        stuff = copy.deepcopy(stuff)
        self.undos.append(stuff)
        self.undo.Enable(True)

    def on_undo(self):

        """Undo the last action
        
        Stores the last change on a stack so that the last change can be redone.
        Pops the previous state of the document before the last change from the
        undo stack."""

        if self.undos:
            stuff = (
                self.sn, 
                self.netlist, 
                self.port_positions, 
                self.wires
            )
            stuff = copy.deepcopy(stuff)
            self.redos.append(stuff)
            stuff = self.undos.pop()
            (
                    self.sn, 
                    self.netlist, 
                    self.port_positions, 
                    self.wires 
            ) = stuff
            self.draw()
            self.redo.Enable(True)
            if not self.undos: self.undo.Enable(False)

    def on_redo(self):

        """Redo the previously undone action
        
        Stores the current state on the undo stack so that the redone change 
        can be undone again. Pops the last undone change from the undo stack.
        """

        if self.redos:
            stuff = (
                self.sn, 
                self.netlist, 
                self.port_positions, 
                self.wires
            )
            stuff = copy.deepcopy(stuff)
            self.undos.append(stuff)
            stuff = self.redos.pop()
            self.sn, self.netlist, self.port_positions, self.wires = stuff
            self.draw()
            self.undo.Enable(True)
            if not self.redos: self.redo.Enable(False)

    def on_left_down(self, event):

        """Capture the mouse left down on an unoccupied schematic area.
        
        By default, this causes the selected component to be placed.
        If a wire is being drawn, a left click places a wire corner."""

        if self.state == "idle":
            component = self.selector.GetSelection()
            component = self.selector.GetItemPyData(component)
            if component is not None:
                self.snapshot()
                instance = str("inst_{0}".format(self.sn))
                self.sn+=1
                self.netlist[instance] = {
                        "component":component, 
                        "parameters": copy.deepcopy(component["parameters"]),
                        "position": snap(event.Coords), 
                        "name": instance
                }
                self.draw()
        elif self.state == "join_port":
            self.snapshot()
            instance = str("inst_{0}".format(self.sn))
            self.sn+=1
            self.netlist[instance] = {
                    "component":components.Bend, 
                    "parameters": copy.deepcopy(components.Bend["parameters"]),
                    "position": snap(event.Coords), 
                    "name":instance
            }
            self.wires.append((
                self.from_instance, 
                self.from_port, 
                instance, 
                "in"
            ))
            self.draw()
            self.state = "idle"

    def on_right_down(self, event):

        """Capture the mouse right down on an unoccupied schematic area.
        
        Causes a schematic context menu to be displayed."""

        if self.state == "idle":
            menu = wx.Menu()
            self.Bind(wx.EVT_MENU, 
                lambda evt: self.export(),
                menu.Append(-1, "export"),
            )
            self.PopupMenu(menu)

    def on_left_up(self, event):

        """Capture the mouse left up on an unoccupied schematic area.
        
        If a block is currently being moved, a left up event causes the
        move operation to terminate."""

        if self.state == "move_block":
            self.state = "idle"

    def on_motion(self, event):

        """Capture the motion event in the schematic area.
        
        If a block move operation is in progress, the block is moved and 
        redrawn. If a wire is being drawn, this event causes a "trace"
        line to be drawn to show the eventual potision of the wire, but does
        not draw the wire yet. if additional performance is needed, it may be
        improved by showing the outline of moving block, but not actualy moving
        the block until a mouse left up event. The undo state is not captured
        for each movement of the block."""

        if self.state == "move_block":
            self.block["position"] = snap(event.Coords)
            self.draw()
        elif self.state == "join_port":
            self.trace.SetPoints([self.from_port_position, snap(event.Coords)])
            self.canvas.Draw(True)

    def on_block_left_down(self, instance):

        """Capture the mouse left down event on a block.
        
        This causes a block move operation to commence, and the current drawing
        state is captured."""

        if self.state == "idle":
            self.state = "move_block"
            self.snapshot()
            self.block = instance

    def on_block_right_down(self, instance):

        """Capture the mouse right down event on a block.
        
        This causes a  block related context menu to be displayed.
        * Edit parameters displays a parameter editing dialog to be displayed.
        * Delete causes the block to be deleted. """

        if self.state == "idle":
            menu = wx.Menu()
            self.Bind(wx.EVT_MENU, 
                lambda evt: self.edit_parameters(
                    instance["parameters"]
                ),
                menu.Append(-1, "Edit Parameters"),
            )
            self.Bind(wx.EVT_MENU, 
                lambda evt: self.delete_instance(instance),
                menu.Append(-1, "Delete"),
            )
            self.PopupMenu(menu)

    def on_out_port_left_down(self, instance_name, port_name):

        """Capture the mouse left down event on a block output port.

        This causes a wire drawing operation to commence."""

        if self.state == "idle":
            if (instance_name not in self.netlist or
                port_name not in self.netlist[instance_name]):
                self.from_instance = instance_name
                self.from_port = port_name
                self.from_port_position = self.port_positions[instance_name][port_name] 
                position = self.port_positions[instance_name][port_name] 
                self.trace = self.canvas.AddLine(
                    (position, position),
                    LineStyle = "LongDash",
                    LineColor = "grey",
                    LineWidth = 1
                )
                self.state = "join_port"

    def on_in_port_left_down(self, instance_name, port_name):

        """Capture the mouse left down event on a block input port.

        If a wire draw operation is in progress, this causes a wire to be
        drawn, and the wire drawing operation to terminate."""

        if self.state == "join_port":
            self.snapshot()
            self.wires.append((
                self.from_instance, 
                self.from_port, 
                instance_name, 
                port_name
            ))
            self.draw()
            self.state = "idle"

    def on_wire_right_down(self, wire):

        """Capture the mouse right down event on a wire.

        This causes a context menu relating to the wire to be displayed::
        * Delete - deletes the wire
        * Tee - breaks the wire and placed a Tee object at the mid point.
        * Bend - breaks the wire and places a Bend object at the mid point.
        """

        if self.state == "idle":
            menu = wx.Menu()
            self.Bind(wx.EVT_MENU, 
                lambda evt: self.disconnect(wire),
                menu.Append(-1, "Delete"),
            )
            self.Bind(wx.EVT_MENU, 
                lambda evt: self.tee(wire),
                menu.Append(-1, "Tee"),
            )
            self.Bind(wx.EVT_MENU, 
                lambda evt: self.bend(wire),
                menu.Append(-1, "Bend"),
            )
            self.PopupMenu(menu)

    def edit_parameters(self, parameters):

        """Launch a parameter editing dialog."""

        dlg = ParameterDlg(parameters, self)
        dlg.ShowModal()

    def bend(self, wire):

        """Break wire and place a Bend object at the mid point."""

        self.snapshot()
        from_instance, from_port, to_instance, to_port = wire
        x1, y1 = self.port_positions[from_instance][from_port]
        x2, y2 = self.port_positions[to_instance][to_port]
        self.disconnect(wire)
        instance = str("inst_{0}".format(self.sn))
        self.sn+=1
        self.netlist[instance] = {
                "component":components.Bend, 
                "parameters": copy.deepcopy(components.Bend["parameters"]),
                "position": snap(((x1+x2)/2, (y1+y2)/2)), 
                "name":instance
        }
        self.wires.append((from_instance, from_port, instance, "in"))
        self.wires.append((instance, "out", to_instance, to_port))
        self.draw()

    def tee(self, wire):

        """Break wire and place a Tee object at the mid point."""

        self.snapshot()
        from_instance, from_port, to_instance, to_port = wire
        x1, y1 = self.port_positions[from_instance][from_port]
        x2, y2 = self.port_positions[to_instance][to_port]
        self.disconnect(wire)
        instance = str("inst_{0}".format(self.sn))
        self.sn+=1
        self.netlist[instance] = {
                "component":components.Tee, 
                "parameters": copy.deepcopy(components.Tee["parameters"]),
                "position": snap(((x1+x2)/2, (y1+y2)/2)), 
                "name":instance
        }
        self.wires.append((from_instance, from_port, instance, "in"))
        self.wires.append((instance, "out1", to_instance, to_port))
        self.draw()

    def delete_instance(self, instance):

        """Delete a component instance, and all conected wires"""

        self.snapshot()
        self.netlist.pop(instance["name"])
        wires = [] 
        for wire in self.wires:
            if (wire[0] != instance["name"] and wire[2] != instance["name"]): 
                wires.append(wire)
        self.wires = wires
        self.draw()

    def disconnect(self, wire):

        """Delete a wire"""

        self.snapshot()
        wires = []
        for w in self.wires:
            if w != wire:
                wires.append(w)
        self.wires = wires
        self.draw()

    def draw(self):

        """Draw the document objects to the schematic editor"""

        self.canvas.ClearAll()
        for instance in self.netlist.values():
            Block(self, instance)
        for wire in self.wires:
            Wire(self, wire)
        self.canvas.Draw(True)

class PythonExpValidator(wx.PyValidator):

    """A python expression validator.
    
    * Tranfers Data to and from windows in a dialog box.
    * Checks that entered data is a valid python expression
    """

    def __init__(self, parameters, parameter):
        wx.PyValidator.__init__(self)
        self.parameter = parameter
        self.parameters = parameters
    def Clone(self):
        return PythonExpValidator(self.parameters, self.parameter)
    def Validate(self, win):
        textctrl = self.GetWindow()
        text = textctrl.GetValue()
        try:
            eval(text)
            textctrl.SetBackgroundColour(
                wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
            )
            textctrl.Refresh()
        except Exception as inst:
            valid = False
            wx.MessageBox(
            """Parameter must be a valid python expression
            {0} 
            raised the following exception:
            {1}""".format(text, inst))
            textctrl.SetBackgroundColour("pink")
            textctrl.SetFocus()
            textctrl.Refresh()
            return False
        return True

    def TransferToWindow(self):
        self.GetWindow().SetValue(
            repr(self.parameters[self.parameter])
        )
        return True

    def TransferFromWindow(self):
        text = self.GetWindow().GetValue()
        self.parameters[self.parameter] = eval(text)
        return True


class ParameterDlg(wx.Dialog):

    """Parameter Editing Dialog.
    
    * Contains a scrolled area with a text box for each parameter.
    * Contains a non-scrolled area with standard dialog buttons.
    """

    def __init__(self, parameters, *args, **kwargs):
        wx.Dialog.__init__(self, *args, **kwargs)
        self.SetExtraStyle(wx.WS_EX_VALIDATE_RECURSIVELY)
        panel = ScrolledPanel(self, -1)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        for parameter in parameters:
            sb = wx.StaticBox(panel, -1, str(parameter))
            hsizer = wx.StaticBoxSizer(sb, wx.HORIZONTAL)
            hsizer.Add(wx.TextCtrl(
                panel, 
                validator=PythonExpValidator(parameters, parameter)
            ), 1, wx.ALIGN_CENTER)
            vsizer.Add(hsizer, 0, wx.EXPAND)
        panel.SetSizer(vsizer)
        panel.SetupScrolling()
        wvsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(wx.Button(self, wx.ID_OK, "OK"), 0, wx.ALIGN_BOTTOM)
        hsizer.Add(wx.Button(self, wx.ID_CANCEL, "Cancel"), 0, wx.ALIGN_BOTTOM)
        wvsizer.Add(panel, 1, wx.EXPAND)
        wvsizer.Add(hsizer, 0, wx.ALIGN_RIGHT)
        self.SetSizer(wvsizer)

def snap(coord):

    """For a coordinate, returns the nearest grid coordinate"""

    x, y = coord
    x = ((x+10)//20)*20
    y = ((y+10)//20)*20
    return x, y

class Wire:

    """Draw the wire described by the wire object"""

    def __init__(self, blockframe, wire):
        from_instance, from_port, to_instance, to_port = wire
        start = blockframe.port_positions[from_instance][from_port]
        end = blockframe.port_positions[to_instance][to_port]
        line = blockframe.canvas.AddLine(
            [start, end], 
            LineWidth = 3, 
            LineColor = "green"
        )
        line.HitLineWidth = 6
        line.Bind(
            FloatCanvas.EVT_FC_RIGHT_DOWN, 
            lambda obj : blockframe.on_wire_right_down((
                from_instance, 
                from_port, 
                to_instance, 
                to_port
            ))
        )

class Block:

    """Draw the block described by the instance object"""

    def __init__(self, blockframe, instance):

        """Draw a block and its port_positions"""

        blockframe = blockframe
        instance = instance

        x, y = instance["position"]
        instance_name = instance["name"]
        name = instance["component"]["name"]
        input_ports = instance["component"]["input_ports"]
        output_ports = instance["component"]["output_ports"]

        height = max([len(input_ports), len(output_ports)])*20 + 20
        width = max((
                max([len(i) for i in input_ports] + [0]) +
                max([len(i) for i in output_ports] + [0])
        ) * 10, len(name) * 10, 100)

        if name not in ["Tee", "Bend"]:
            outline = blockframe.canvas.AddRectangle(
                    (x, y), 
                    (width, height+20),
                    LineWidth = 3,
                    LineColor = "blue",
            )

            title = blockframe.canvas.AddScaledText(
                    name,
                    (x+10, y+height+10),
                    10
            )

        else:
            outline = blockframe.canvas.AddCircle(
                    (x, y), 
                    10,
                    LineWidth = 1,
                    LineColor = "green",
            )
            width = 0
        outline.PutInForeground()

        outline.Bind(
            FloatCanvas.EVT_FC_LEFT_DOWN, 
            lambda obj : blockframe.on_block_left_down(instance)
        )

        outline.Bind(
            FloatCanvas.EVT_FC_RIGHT_DOWN, 
            lambda obj : blockframe.on_block_right_down(instance)
        )

        blockframe.port_positions[instance_name] = {}
        connected = [
                wire[3] for 
                wire in 
                blockframe.wires if 
                wire[2] == instance_name
        ]

        y_offset = height - 20
        for port_name in input_ports:
            if port_name not in connected:
                def callback(obj, 
                        instance_name=instance_name, 
                        port_name=port_name):
                    blockframe.on_in_port_left_down(
                        instance_name, 
                        port_name
                    )
                if name in ["Tee", "Bend"]:
                    outline = blockframe.canvas.AddCircle(
                        (x-10, y), 
                        10,
                        LineColor = "red",
                        LineWidth = 1
                    )
                else:
                    outline = blockframe.canvas.AddCircle(
                        (x, y+y_offset), 
                        10,
                        LineColor = "red",
                        LineWidth = 1
                    )
                outline.Bind(
                    FloatCanvas.EVT_FC_LEFT_DOWN, 
                    callback
                )
            if name not in ["Tee", "Bend"]:
                blockframe.port_positions[instance_name][port_name] = (
                    x, 
                    y+y_offset
                )
                blockframe.canvas.AddScaledText(
                    port_name,
                    (x+10, y+y_offset),
                    10,
                    Position = "cl",
                )
            else:
                blockframe.port_positions[instance_name][port_name] = (x, y)
            outline.PutInForeground()
            y_offset -= 20

        connected = [
            wire[1] for 
            wire in 
            blockframe.wires if 
            wire[0] == instance_name
        ]

        y_offset = height - 20
        for port_name in output_ports:
            if port_name not in connected:
                def callback(obj,
                        instance_name=instance_name,
                        port_name=port_name):
                    blockframe.on_out_port_left_down(
                        instance_name, 
                        port_name
                    )
                if name in ["Tee", "Bend"]:
                    outline = blockframe.canvas.AddCircle(
                        (x+10, y), 
                        10,
                        LineColor = "red",
                        LineWidth = 1
                    )
                else:
                    outline = blockframe.canvas.AddCircle(
                        (x+width, y+y_offset),
                        10,
                        LineColor = "red",
                    )
                outline.Bind(
                    FloatCanvas.EVT_FC_LEFT_DOWN, 
                    callback
                )
            if name not in ["Tee", "Bend"]:
                blockframe.port_positions[instance_name][port_name] = (
                    x+width, 
                    y+y_offset
                )
                blockframe.canvas.AddScaledText(
                        port_name,
                        (x+width-10, y+y_offset),
                        10,
                        Position = "cr"
                )
            else:
                blockframe.port_positions[instance_name][port_name] = (x, y)
            outline.PutInForeground()
            y_offset -= 20

#Create an application and show the main window
app = wx.App()
BlockFrame(None, size=(1024,768), title="Schematix").Show()
app.MainLoop()
