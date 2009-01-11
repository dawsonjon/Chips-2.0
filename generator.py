library = """
def Bend(a):
    return a

def Tee(a):
    temp = Variable(0)
    x = Output()
    y = Output()
    Process(a.get_bits(),
        Loop(
            a.read(temp),
            x.write(temp),
            y.write(temp),
        )
    )
    return x, y

def Mul(a, b):
    return a * b

def Div(a, b):
    return a // b

def Add(a, b):
    return a + b

def Sub(a, b):
    return a - b

def AND(a, b):
    return a & b

def OR(a, b):
    return a | b

def XOR(a, b):
    return a ^ b

def NOT(a):
    return ~a

def Eq(a, b):
    return a == b

def Ne(a, b):
    return a != b

def Lt(a, b):
    return a < b

def Gt(a, b):
    return a > b

def Le(a, b):
    return a <= b

def Ge(a, b):
    return a >= b
"""


def generate(filename, netlist, ports, wires):

    """Generate a Chips file from the schematic"""

    output_file = open(filename, "w")

    generated_streams = {}
    generated_instances = {}
    generated_sinks = {}

    #check if all the input streams for a block have been created
    #============================================================
    output_file.write("from chips import *\n\n")
    output_file.write(library)

    all_streams_generated = False
    while not all_streams_generated:
        all_streams_generated = True
        for instance in netlist.values():

            #check if all the input streams for a block have been created
            #============================================================
            all_input_streams_exist = True
            for port_name in instance["component"]["input_ports"]:
                full_port_name = instance["name"]+"_"+port_name
                if full_port_name not in generated_streams:
                    all_input_streams_exist = False
                    all_streams_generated = False

            #if they have, check whether the block has been created
            #======================================================
            if all_input_streams_exist:
                if instance["name"] not in generated_instances:
                    #list input streams
                    #------------------
                    in_streams = []
                    for port_name in instance["component"]["input_ports"]:
                        stream = instance["name"]+"_"+port_name
                        in_streams.append(stream)
                        generated_streams[stream]=stream

                    #list output streams
                    #-------------------
                    out_streams = []
                    for port_name in instance["component"]["output_ports"]:
                        for wire in wires:
                            if wire[0] == instance["name"] and wire[1] == port_name:
                                stream = wire[2] + "_" + wire[3]
                                break
                        #add new streams to stream list
                        generated_streams[stream]=stream
                        out_streams.append(stream)

                    #generate component
                    #------------------
                    parameters = [
                        str(i) + "=" + repr(j) for 
                        i, j in 
                        instance["parameters"].iteritems()
                    ]
                    if not instance["component"]["output_ports"]:
                        #must be a sink
                        output_file.write("{0} = {1}({2})\n".format(
                            instance["name"],
                            instance["component"]["function"],
                            ", ".join(in_streams + parameters),
                        ))
                        generated_sinks[instance["name"]] = instance["name"]
                    else:
                        output_file.write("{0} = {1}({2})\n".format(
                            ", ".join(out_streams),
                            instance["component"]["function"],
                            ", ".join(in_streams + parameters),
                        ))
                    generated_instances[instance["name"]] = instance["name"]

    #if they have, check whether the block has been created
    #======================================================
    output_file.write("\nchip = Chip(\n    {0}\n)\n".format(
        ",\n    ".join(generated_sinks.values())
    ))
    output_file.write("chip.reset()\n")
    output_file.write("chip.execute(10000)\n")

