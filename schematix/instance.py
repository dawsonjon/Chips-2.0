import wx
from wx.lib.floatcanvas import NavCanvas, FloatCanvas, Resources

class Instance():

    """A graphical representation of an instance"""

    def __init__(self, blockframe, instance):

        """Draw a block and its port_positions"""

        x, y = instance["position"]
        instance_name = instance["name"]
        name = instance["component"]["name"]
        input_ports = instance["component"]["inputs"]
        output_ports = instance["component"]["outputs"]

        #calculate the size of the block based on the width of text
        #and the number of ports

        height = max([len(input_ports), len(output_ports)])*20 + 40
        width = max((
                max([len(i) for i in input_ports] + [0]) +
                max([len(i) for i in output_ports] + [0])
        ) * 10, len(name) * 10, 100)

        if name in ["tee", "bend"]:

            #Tees and bends look like green circles

            outline = blockframe.canvas.AddCircle(
                    (x, y), 
                    10,
                    LineWidth = 1,
                    LineColor = "green",
            )

            width = 10
            height = 10
            style = "node"

        elif name in ["input", "output"]:

            #Input and output ports are blue circles

            outline = blockframe.canvas.AddCircle(
                    (x, y), 
                    10,
                    LineWidth = 1,
                    LineColor = "blue",
            )

            width = 10
            height = 10
            style = "port"

        else:

            #Normal blocks are blue rectangles

            outline = blockframe.canvas.AddRectangle(
                    (x, y), 
                    (width, height),
                    LineWidth = 3,
                    LineColor = "blue",
            )

            title = blockframe.canvas.AddScaledText(
                    name,
                    (x+10, y+height-10),
                    10
            )

            style = "normal"


        outline.PutInForeground()

        outline.Bind(
            FloatCanvas.EVT_FC_LEFT_DOWN, 
            lambda obj : blockframe.on_block_left_down(instance, (width, height), style)
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

        y_offset = height - 40
        for port_name in input_ports:

            #Symbol

            if port_name not in connected:
                #the red circle is only drawn if the port is unconnected

                def callback(obj, 
                        instance_name=instance_name, 
                        port_name=port_name):
                    blockframe.on_in_port_left_down(
                        instance_name, 
                        port_name
                    )

                if name in ["tee", "bend", "input", "output"]:
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

            #Label

            if name in ["tee", "bend"]:

                #ports have no labels on tees or bends

                blockframe.port_positions[instance_name][port_name] = (x, y)

            elif name in ["input", "output"]:

                #ports have a simple label in input and output ports

                blockframe.port_positions[instance_name][port_name] = (x, y)
                blockframe.canvas.AddScaledText(
                    instance["port_name"],
                    (x+10, y),
                    10,
                    Position = "cl",
                )

            else:

                #ports have a simple label in normal components

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
            outline.PutInForeground()
            y_offset -= 20

        connected = [
            wire[1] for 
            wire in 
            blockframe.wires if 
            wire[0] == instance_name
        ]

        #Draw input ports

        y_offset = height - 40
        for port_name in output_ports:

            #Symbol

            if port_name not in connected:

                #The red circle is only drawn if the port is unconnected

                def callback(obj,
                        instance_name=instance_name,
                        port_name=port_name):
                    blockframe.on_out_port_left_down(
                        instance_name, 
                        port_name
                    )

                if name in ["tee", "bend", "input", "output"]:
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

            #Label

            if name in ["tee", "bend"]:

                #ports have no labels on tees or bends

                blockframe.port_positions[instance_name][port_name] = (x, y)

            elif name in["input", "output"]:

                #ports have a simple label in input and output ports

                blockframe.port_positions[instance_name][port_name] = (x, y)
                blockframe.canvas.AddScaledText(
                        instance["port_name"],
                        (x-width, y),
                        10,
                        Position = "cr"
                )
            else:

                #ports have a simple label in normal components

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

            outline.PutInForeground()
            y_offset -= 20
