import wx
from wx.lib.floatcanvas import NavCanvas, FloatCanvas, Resources


class Wire:
    def __init__(self, blockframe):
        self.blockframe = blockframe

    def draw(self):
        if hasattr(self, "traceline"):
            self.blockframe.canvas.RemoveObject(self.traceline)
            del self.traceline
        if hasattr(self, "wire"):
            self.wire.SetPoints([self.start_point, self.end_point])
        else:
            self.wire = self.blockframe.canvas.AddLine(
                    [self.start_point,
                     self.end_point],
                    LineWidth=3,
                    LineColor="dark green"
            )
        self.blockframe.canvas.Draw(True)

    def trace(self, coord):
        if hasattr(self, "traceline"):
            self.traceline.SetPoints([self.start_point, coord])
        else:
            self.traceline = self.blockframe.canvas.AddLine(
                    [self.start_point,
                     coord],
                    LineWidth=2,
                    LineStyle="ShortDash",
                    LineColor="light grey"
            )
        self.blockframe.canvas.Draw(True)

class InPort:
    def __init__(self, blockframe, position, label, style = "normal"):
        self.blockframe = blockframe
        self.rectangle = self.blockframe.canvas.AddCircle(
                position, 
                10,
                LineColor = "dark green")
        self.rectangle.Bind(
                FloatCanvas.EVT_FC_LEFT_DOWN, 
                lambda obj: self.blockframe.on_in_port_left_down(self)
        )
        if style != "normal":
            self.rectangle.Hide()
        self.position = position

    def move(self, coord):
        self.rectangle.SetPoint(coord)
        self.position = coord
        if hasattr(self, "wire"):
            self.wire.end_point = coord
            self.wire.draw()

    def terminate_wire(self, wire):
        self.wire = wire
        wire.end_point = self.position
        wire.draw()

class OutPort:
    def __init__(self, blockframe, position, label, style = "normal"):
        self.blockframe = blockframe
        self.rectangle = self.blockframe.canvas.AddCircle(
                position, 
                10,
                LineColor = "dark green")
        self.rectangle.Bind(
                FloatCanvas.EVT_FC_LEFT_DOWN, 
                lambda obj: self.blockframe.on_out_port_left_down(self)
        )
        if style != "normal":
            self.rectangle.Hide()
        self.position = position

    def move(self, coord):
        self.rectangle.SetPoint(coord)
        self.position = coord
        if hasattr(self, "wire"):
            self.wire.start_point = coord
            self.wire.draw()

    def start_wire(self):
        if hasattr(self, "wire"):
            return None
        self.wire = Wire(self.blockframe)
        self.wire.start_point = self.position
        return self.wire

class WireHandle:
    def __init__(self, blockframe, position):
        self.blockframe = blockframe
        self.inport = InPort(blockframe, position, None, "wirehandle")
        self.outport = OutPort(blockframe, position, None, "wirehandle")
        self.rectangle = self.blockframe.canvas.AddCircle(
                position, 
                8,
                FillColor = "dark green"
        )
        self.rectangle.Bind(
            FloatCanvas.EVT_FC_LEFT_DOWN, 
            lambda obj : blockframe.on_block_left_down(self)
        )

    def move(self, position):
        self.rectangle.SetPoint(position)
        self.inport.move(position)
        self.outport.move(position)
        self.blockframe.canvas.Draw(True)

class Block:
    def __init__(self, blockframe, position, input_ports, output_ports):
        self.blockframe = blockframe
        x, y = position
        self.height = max([len(input_ports), len(output_ports)])*20 + 20

        self.rectangle = self.blockframe.canvas.AddRectangle(
                position, 
                (100, self.height),
                LineWidth = 3,
                LineColor = "dark green",
                FillColor = "light green"
        )

        self.rectangle.Bind(
            FloatCanvas.EVT_FC_LEFT_DOWN, 
            lambda obj : blockframe.on_block_left_down(self)
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
                        (x+100, y+y_offset), 
                        i
                    )
            )
            y_offset -= 20

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
            i.move((x+100, y+y_offset)) 
            y_offset -= 20
        self.blockframe.canvas.Draw(True)

class BlockFrame(wx.Frame):
    def __init__(self, *args, **kwargs):

        #draw windows
        wx.Frame.__init__(self, *args, **kwargs)
        canvas = NavCanvas.NavCanvas(self)
        self.canvas = canvas.Canvas
        self.rect = self.canvas.AddRectangle((10, 10), (20, 20))
        self.blocks = []

        #bind events
        self.state = "idle"
        self.canvas.Bind(FloatCanvas.EVT_LEFT_UP, self.on_left_up)
        self.canvas.Bind(FloatCanvas.EVT_LEFT_DOWN, self.on_left_down)
        self.canvas.Bind(FloatCanvas.EVT_MOTION, self.on_motion)

    def on_left_down(self, event):
        print "left_down", event.Coords
        if self.state == "idle":
            Block(self, event.Coords, ["a", "b", "c"], ["z"])
        elif self.state == "join_port":
            handle = WireHandle(self, event.Coords)
            handle.inport.terminate_wire(self.wire)
            self.wire = handle.outport.start_wire()

    def on_left_up(self, event):
        print "left_up", event.Coords
        if self.state == "move_block":
            self.state = "idle"

    def on_motion(self, event):
        print "motion", event.Coords
        if self.state == "move_block":
            self.block.move(event.Coords)
            self.canvas.Draw(True)
        elif self.state == "join_port":
            self.wire.trace(event.Coords)
            self.canvas.Draw(True)

    def on_block_left_down(self, block):
        print "block left down"
        self.state = "move_block"
        self.block = block

    def on_out_port_left_down(self, port):
        print "out port left down"
        self.wire = port.start_wire()
        if self.wire is not None:
            self.state = "join_port"

    def on_in_port_left_down(self, port):
        print "in port left up"
        if self.state == "join_port":
            port.terminate_wire(self.wire)
            self.state = "idle"



app = wx.App()
BlockFrame(None, size=(1024,768), title="Scematic editor").Show()
app.MainLoop()
