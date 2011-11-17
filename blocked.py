import wx
from wx.lib.floatcanvas import NavCanvas, FloatCanvas, Resources


class InPort:
    def __init__(self, blockframe, position, label):
        self.blockframe = blockframe
        self.connected = False
        self.rectangle = self.blockframe.canvas.AddCircle(
                position, 
                10,
                LineColor = "dark green"
        )
        self.rectangle.Bind(
                FloatCanvas.EVT_FC_LEFT_DOWN, 
                lambda obj: self.blockframe.on_in_port_left_down(self)
        )
        if label is not None:
            x, y = position
            self.label = self.blockframe.canvas.AddScaledText(
                label,
                (x+10, y),
                10,
                Position = "cl",
            )
        self.position = position

    def move(self, coord):
        self.rectangle.SetPoint(coord)
        self.position = coord
        if self.connected:
            self.out_port.draw_wire()
        if hasattr(self, "label"):
            x, y = coord
            self.label.SetPoint(
                (x+10, y),
            )

    def delete(self):
        self.blockframe.canvas.RemoveObject(self.rectangle)
        if self.connected:
            self.out_port.disconnect()
        if hasattr(self, "label"):
            self.blockframe.canvas.RemoveObject(self.label)
        self.blockframe.canvas.Draw(True)

class OutPort:
    def __init__(self, blockframe, position, label):
        self.connected = False
        self.blockframe = blockframe
        self.rectangle = self.blockframe.canvas.AddCircle(
                position, 
                10,
                LineColor = "dark green")
        self.rectangle.Bind(
                FloatCanvas.EVT_FC_LEFT_DOWN, 
                lambda obj: self.blockframe.on_out_port_left_down(self)
        )
        if label is not None:
            x, y = position
            self.label = self.blockframe.canvas.AddScaledText(
                    label,
                    (x-10, y),
                    10,
                    Position = "cr"
            )
        self.position = position

    def draw_wire(self):
        if hasattr(self, "in_port"):
            self.wire.SetPoints([self.position, self.in_port.position])
            self.blockframe.canvas.Draw(True)

    def move(self, coord):
        self.rectangle.SetPoint(coord)
        self.position = coord
        if hasattr(self, "label"):
            x, y = coord
            self.label.SetPoint(
                (x-10, y),
            )
        self.draw_wire()

    def delete(self):
        self.blockframe.canvas.RemoveObject(self.rectangle)
        if self.connected:
            self.disconnect()
        if hasattr(self, "label"):
            self.blockframe.canvas.RemoveObject(self.label)
        self.blockframe.canvas.Draw(True)

    def disconnect(self):
        if self.connected:
            self.in_port.connected = False
            self.connected = False
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
            self.in_port.connected = True
            self.in_port.out_port = self
            self.wire = self.blockframe.canvas.AddLine(
                    [self.position, self.in_port.position],
                    LineColor = "dark green",
                    LineWidth = 3
            )
            self.wire.Bind(
                    FloatCanvas.EVT_FC_RIGHT_DOWN, 
                    lambda obj: self.blockframe.on_wire_right_down(self)
            )
            self.blockframe.canvas.Draw(True)

class WireHandle:
    def __init__(self, blockframe, position):
        x, y = position
        self.blockframe = blockframe
        self.inport = InPort(blockframe, (x-8, y), None)
        self.outport1 = OutPort(blockframe, (x, y+8), None)
        self.outport2 = OutPort(blockframe, (x, y-8), None)
        self.rectangle = self.blockframe.canvas.AddCircle(
                position, 
                8,
                FillColor = "dark green"
        )
        self.rectangle.Bind(
            FloatCanvas.EVT_FC_LEFT_DOWN, 
            lambda obj : blockframe.on_block_left_down(self)
        )
        self.rectangle.Bind(
            FloatCanvas.EVT_FC_RIGHT_DOWN, 
            lambda obj : blockframe.on_block_right_down(self)
        )

    def delete(self):
        self.blockframe.canvas.RemoveObject(self.rectangle)
        self.inport.delete()
        self.outport1.delete()
        self.outport2.delete()
        self.blockframe.canvas.Draw(True)

    def move(self, position):
        x, y = position
        self.rectangle.SetPoint(position)
        self.inport.move((x-8, y))
        self.outport1.move((x, y+8))
        self.outport2.move((x, y-8))
        self.blockframe.canvas.Draw(True)

class Block:
    def __init__(self, blockframe, position, input_ports, output_ports, title):
        self.blockframe = blockframe
        x, y = position

        self.height = max([len(input_ports), len(output_ports)])*20 + 20
        self.width = max((
            max([len(i) for i in input_ports]) +
            max([len(i) for i in output_ports])
        ) * 10, 100)

        self.rectangle = self.blockframe.canvas.AddRectangle(
                position, 
                (self.width, self.height+20),
                LineWidth = 3,
                LineColor = "dark green",
                FillColor = "light green"
        )

        self.title = self.blockframe.canvas.AddScaledText(
                title,
                (x+10, y+self.height+10),
                10
        )

        self.rectangle.Bind(
            FloatCanvas.EVT_FC_LEFT_DOWN, 
            lambda obj : blockframe.on_block_left_down(self)
        )

        self.rectangle.Bind(
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
        self.blockframe.canvas.RemoveObject(self.rectangle)
        self.blockframe.canvas.RemoveObject(self.title)
        for i in self.input_ports:
            i.delete()
        for i in self.output_ports:
            i.delete()
        self.blockframe.canvas.Draw(True)

    def move(self, coord):
        x, y = coord
        x, y = x - 50 , y - self.height/2
        self.rectangle.SetPoint((x, y))
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
        canvas = NavCanvas.NavCanvas(self)
        self.canvas = canvas.Canvas
        self.rect = self.canvas.AddCircle((0, 0), 20)
        self.blocks = []

        #bind events
        self.state = "idle"
        self.canvas.Bind(FloatCanvas.EVT_LEFT_UP, self.on_left_up)
        self.canvas.Bind(FloatCanvas.EVT_LEFT_DOWN, self.on_left_down)
        self.canvas.Bind(FloatCanvas.EVT_MOTION, self.on_motion)

    def on_left_down(self, event):
        if self.state == "idle":
            Block(self, event.Coords, ["a", "b", "c"], ["blah"], "a block")
        elif self.state == "join_port":
            handle = WireHandle(self, event.Coords)
            self.port_from.connect(handle.inport)
            self.canvas.RemoveObject(self.trace)
            self.canvas.Draw(True)
            self.state = "idle"

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
                lambda evt: self.split(port),
                menu.Append(-1, "split"),
            )
            self.PopupMenu(menu)

    def split(self, from_port):
        to_port = from_port.in_port
        from_port.disconnect()
        x1, y1, x2, y2 = from_port.position + to_port.position
        handle = WireHandle(self, ((x1+x2)/2, (y1+y2)/2))
        from_port.connect(handle.inport)
        handle.outport1.connect(to_port)

app = wx.App()
BlockFrame(None, size=(1024,768), title="Schematic editor").Show()
app.MainLoop()
