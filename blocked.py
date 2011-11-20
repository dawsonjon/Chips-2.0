#!/usr/bin/env python

import wx
from wx.lib.floatcanvas import NavCanvas, FloatCanvas, Resources

import components

class InPort:
    def __init__(self, blockframe, position, label):
        self.blockframe = blockframe
        self.connected = False
        self.position = position
        x, y = position
        self.outline = self.blockframe.canvas.AddCircle(
            (x-10, y), 
            10,
            LineColor = "red",
            LineWidth = 1
        )
        self.outline.PutInForeground()
        self.outline.Bind(
                FloatCanvas.EVT_FC_LEFT_DOWN, 
                lambda obj: self.blockframe.on_in_port_left_down(self)
        )
        if label is not None:
            self.label = self.blockframe.canvas.AddScaledText(
                label,
                (x+10, y),
                10,
                Position = "cl",
            )

    def hide(self):
        self.outline.Hide()

    def show(self):
        self.outline.Show()

    def move(self, postion):
        self.position = postion
        x, y = postion
        self.outline.SetPoint((x-10, y))
        if self.connected:
            self.out_port.draw_wire()
        if hasattr(self, "label"):
            self.label.SetPoint(
                (x+10, y),
            )

    def delete(self):
        self.blockframe.canvas.RemoveObject(self.outline)
        if self.connected:
            self.out_port.disconnect()
        if hasattr(self, "label"):
            self.blockframe.canvas.RemoveObject(self.label)
        self.blockframe.canvas.Draw(True)

class OutPort:
    def __init__(self, blockframe, position, label):
        self.connected = False
        self.blockframe = blockframe
        x, y = position
        self.position = position
        self.outline = self.blockframe.canvas.AddCircle(
            (x+10, y),
            10,
            LineColor = "red",
        )
        self.outline.PutInForeground()
        self.outline.Bind(
                FloatCanvas.EVT_FC_LEFT_DOWN, 
                lambda obj: self.blockframe.on_out_port_left_down(self)
        )
        if label is not None:
            self.label = self.blockframe.canvas.AddScaledText(
                    label,
                    (x-5, y),
                    10,
                    Position = "cr"
            )

    def draw_wire(self):
        if hasattr(self, "in_port"):
            self.wire.SetPoints([self.position, self.in_port.position])
            self.blockframe.canvas.Draw(True)

    def hide(self):
        self.outline.Hide()

    def show(self):
        self.outline.Show()

    def move(self, postion):
        self.position = postion
        x, y = postion
        self.outline.SetPoint((x+10, y))
        if hasattr(self, "label"):
            self.label.SetPoint(
                (x-10, y),
            )
        self.draw_wire()

    def delete(self):
        self.blockframe.canvas.RemoveObject(self.outline)
        if self.connected:
            self.disconnect()
        if hasattr(self, "label"):
            self.blockframe.canvas.RemoveObject(self.label)
        self.blockframe.canvas.Draw(True)

    def disconnect(self):
        if self.connected:
            self.in_port.connected = False
            self.in_port.show()
            self.connected = False
            self.show()
            del self.in_port.out_port
            del self.in_port
            self.blockframe.canvas.RemoveObject(self.wire)
            self.blockframe.canvas.Draw(True)

    def connect(self, in_port):
        if self.connected:
            return False
        else:
            self.connected = True
            self.in_port = in_port
            self.hide()
            self.in_port.connected = True
            self.in_port.hide()
            self.in_port.out_port = self
            self.wire = self.blockframe.canvas.AddLine(
                    [self.position, self.in_port.position],
                    LineColor = "green",
                    LineWidth = 2,
            )
            self.wire.HitLineWidth = 6
            self.wire.PutInBackground()
            self.wire.Bind(
                    FloatCanvas.EVT_FC_RIGHT_DOWN, 
                    lambda obj: self.blockframe.on_wire_right_down(self)
            )
            self.blockframe.canvas.Draw(True)

class Bend:
    def __init__(self, blockframe, position):
        x, y = position
        self.blockframe = blockframe
        self.outline = self.blockframe.canvas.AddCircle(
            position,
            10,
            LineColor = "green"
        )
        self.outline.PutInForeground()
        self.inport = InPort(blockframe, position, None)
        self.outport = OutPort(blockframe, position, None)
        self.outline.Bind(
            FloatCanvas.EVT_FC_LEFT_DOWN, 
            lambda obj : blockframe.on_block_left_down(self)
        )
        self.outline.Bind(
            FloatCanvas.EVT_FC_RIGHT_DOWN, 
            lambda obj : blockframe.on_block_right_down(self)
        )

    def delete(self):
        self.blockframe.canvas.RemoveObject(self.outline)
        self.inport.delete()
        self.outport.delete()
        self.blockframe.canvas.Draw(True)

    def move(self, position):
        self.outline.SetPoint(position)
        self.inport.move(position)
        self.outport.move(position)
        self.blockframe.canvas.Draw(True)

class Tee:
    def __init__(self, blockframe, position):
        self.blockframe = blockframe
        self.outline = self.blockframe.canvas.AddCircle(
            position,
            10,
            FillColor = "green",
            LineColor = "green"
        )
        self.outline.PutInForeground()
        self.inport = InPort(blockframe, position, None)
        self.outport1 = OutPort(blockframe, position, None)
        self.outport2 = OutPort(blockframe, position, None)
        self.outline.Bind(
            FloatCanvas.EVT_FC_LEFT_DOWN, 
            lambda obj : blockframe.on_block_left_down(self)
        )
        self.outline.Bind(
            FloatCanvas.EVT_FC_RIGHT_DOWN, 
            lambda obj : blockframe.on_block_right_down(self)
        )

    def delete(self):
        self.blockframe.canvas.RemoveObject(self.outline)
        self.inport.delete()
        self.outport1.delete()
        self.outport2.delete()
        self.blockframe.canvas.Draw(True)

    def move(self, position):
        self.outline.SetPoint(position)
        self.inport.move(position)
        self.outport1.move(position)
        self.outport2.move(position)
        self.blockframe.canvas.Draw(True)

class Block:
    def __init__(self, blockframe, position, component):
        title, input_ports, output_ports = component
        self.blockframe = blockframe
        self.blockframe.blocks.append(self)
        x, y = position

        self.height = max([len(input_ports), len(output_ports)])*20 + 20
        self.width = max(
            (
                max([len(i) for i in input_ports] + [0]) +
                max([len(i) for i in output_ports] + [0])
            ) * 10, 
            len(title) * 10,
            100
        )

        self.outline = self.blockframe.canvas.AddRectangle(
                position, 
                (self.width, self.height+20),
                LineWidth = 3,
                LineColor = "blue",
        )

        self.title = self.blockframe.canvas.AddScaledText(
                title,
                (x+10, y+self.height+10),
                10
        )

        self.outline.Bind(
            FloatCanvas.EVT_FC_LEFT_DOWN, 
            lambda obj : blockframe.on_block_left_down(self)
        )

        self.outline.Bind(
            FloatCanvas.EVT_FC_RIGHT_DOWN, 
            lambda obj : blockframe.on_block_right_down(self)
        )

        y_offset = self.height - 20
        self.input_ports = []
        for i in input_ports:
            self.input_ports.append(
                    InPort(
                        blockframe, 
                        (x, y+y_offset), 
                        i
                    )
            )
            y_offset -= 20

        self.output_ports = []
        y_offset = self.height - 20
        for i in output_ports:
            self.output_ports.append(
                    OutPort(
                        blockframe, 
                        (x+self.width, y+y_offset), 
                        i
                    )
            )
            y_offset -= 20

        self.blockframe.canvas.Draw(True)

    def delete(self):
        self.blockframe.canvas.RemoveObject(self.outline)
        self.blockframe.canvas.RemoveObject(self.title)
        for i in self.input_ports:
            i.delete()
        for i in self.output_ports:
            i.delete()
        self.blockframe.canvas.Draw(True)
        self.blockframe.blocks.remove(self)

    def move(self, postion):
        x, y = postion
        x, y = x - 50 , y - self.height/2
        self.outline.SetPoint((x, y))
        y_offset = self.height - 20
        for i in self.input_ports:
            i.move((x, y+y_offset)) 
            y_offset -= 20
        y_offset = self.height - 20
        for i in self.output_ports:
            i.move((x+self.width, y+y_offset)) 
            y_offset -= 20
        self.title.SetPoint(
                (x+10, y+self.height+10),
        )
        self.blockframe.canvas.Draw(True)

            



class BlockFrame(wx.Frame):
    def __init__(self, *args, **kwargs):

        #draw windows
        wx.Frame.__init__(self, *args, **kwargs)

        #make canvas
        canvas = NavCanvas.NavCanvas(self, style=wx.SUNKEN_BORDER)
        self.canvas = canvas.Canvas

        #make component selector
        selector = wx.TreeCtrl(self, style=wx.SUNKEN_BORDER|wx.TR_DEFAULT_STYLE)
        root = selector.AddRoot("items")
        for library_name, library in components.components:
            library_node = selector.AppendItem(root, library_name)
            for component in library:
                title = component[0]
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

        self.blocks = []

    def on_left_down(self, event):
        if self.state == "idle":
            component = self.selector.GetSelection()
            component = self.selector.GetItemPyData(component)
            if component is not None:
                title, inputs, outputs = component
                Block(self, event.Coords, component)
        elif self.state == "join_port":
            handle = Bend(self, event.Coords)
            self.port_from.connect(handle.inport)
            self.canvas.RemoveObject(self.trace)
            self.canvas.Draw(True)
            self.state = "idle"

    def on_right_down(self, event):
        if self.state == "idle":
            menu = wx.Menu()
            self.Bind(wx.EVT_MENU, 
                lambda evt: self.export(),
                menu.Append(-1, "export"),
            )
            self.PopupMenu(menu)

    def on_left_up(self, event):
        if self.state == "move_block":
            self.state = "idle"

    def on_motion(self, event):
        if self.state == "move_block":
            self.block.move(event.Coords)
            self.canvas.Draw(True)
        elif self.state == "join_port":
            self.trace.SetPoints([self.port_from.position, event.Coords])
            self.canvas.Draw(True)

    def on_block_left_down(self, block):
        if self.state == "idle":
            self.state = "move_block"
            self.block = block

    def on_block_right_down(self, block):
        if self.state == "idle":
            menu = wx.Menu()
            self.Bind(wx.EVT_MENU, 
                lambda evt: block.delete(),
                menu.Append(-1, "delete"),
            )
            self.PopupMenu(menu)

    def on_out_port_left_down(self, port):
        if self.state == "idle":
            if not port.connected:
                self.port_from = port
                self.trace = self.canvas.AddLine(
                    [port.position, port.position],
                    LineStyle = "LongDash",
                    LineColor = "grey",
                    LineWidth = 1
                )
                self.state = "join_port"

    def on_in_port_left_down(self, port):
        if self.state == "join_port":
            self.port_from.connect(port)
            self.canvas.RemoveObject(self.trace)
            self.canvas.Draw(True)
            self.state = "idle"

    def on_wire_right_down(self, port):
        if self.state == "idle":
            menu = wx.Menu()
            self.Bind(wx.EVT_MENU, 
                lambda evt: port.disconnect(),
                menu.Append(-1, "delete"),
            )
            self.Bind(wx.EVT_MENU, 
                lambda evt: self.tee(port),
                menu.Append(-1, "tee"),
            )
            self.Bind(wx.EVT_MENU, 
                lambda evt: self.bend(port),
                menu.Append(-1, "bend"),
            )
            self.PopupMenu(menu)

    def bend(self, from_port):
        to_port = from_port.in_port
        x1, y1 = from_port.position 
        x2, y2 = to_port.position
        from_port.disconnect()
        handle = Bend(self, ((x1+x2)/2, (y1+y2)/2))
        from_port.connect(handle.inport)
        handle.outport.connect(to_port)

    def tee(self, from_port):
        to_port = from_port.in_port
        x1, y1  = from_port.position 
        x2, y2 = to_port.position
        from_port.disconnect()
        handle = Tee(self, ((x1+x2)/2, (y1+y2)/2))
        from_port.connect(handle.inport)
        handle.outport1.connect(to_port)


app = wx.App()
BlockFrame(None, size=(1024,768), title="Schematic editor").Show()
app.MainLoop()
