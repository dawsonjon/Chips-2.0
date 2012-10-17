import wx
from wx.lib.floatcanvas import NavCanvas, FloatCanvas, Resources

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
