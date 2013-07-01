#!/usr/bin/env python
import os
import pickle

import wx

import schematix

class SchematicError(Exception):
    def __init__(self, message):
        self.message = message

def edit(window, component):

    """Edit a schematic"""

    if component["name"] in window.schematic_windows:
        #window.schematic_windows[component["name"]].SetFocus()
        window.schematic_windows[component["name"]].Raise()
    else:
        schematic = schematix.BlockFrame(window, None, size=(1024,768), title="Schematix")
        schematic.Show()
        schematic.open(window.get_source_path(component))
        window.schematic_windows[component["name"]] = schematic
    window.update()

def _import(window, component):

    """Import an existing schematic"""

    schematic = schematix.BlockFrame(window, None, size=(1024,768), title="Schematix")
    schematic.Show()
    schematic.open(component["source_file"])
    window.update()

def new(window):

    """Make a new schematic"""

    dlg = wx.TextEntryDialog(
        window, 
        "Component name:",
        "New Schematic")
    if dlg.ShowModal() == wx.ID_OK:
        name = dlg.GetValue()
        new_file = name + ".v"
        new_file = os.path.join(
            window.project_path.GetValue(),
            new_file)
        new_file = open(new_file, "w")
        new_file.write("//name : %s\n"%name)
        new_file.write("//source_file : %s\n"%(name+".sch"))
        new_file.close()
        new_file = name + ".sch"
        new_file = os.path.join(
            window.project_path.GetValue(),
            new_file)
        new_file = open(new_file, "w")
        pickle.dump(0, new_file)
        pickle.dump({}, new_file)
        pickle.dump({}, new_file)
        pickle.dump([], new_file)
        pickle.dump("", new_file)
        new_file.close()
        window.update()

def generate_ports(netlist, wires, vhdl):

    """Generate a list of ports and device io."""

    input_ports = {}
    output_ports = {}
    for instance_name, instance in netlist.iteritems():
        if instance["component"]["name"] == "input":
            input_ports[instance["port_name"]] = instance["port_size"]
            vhdl.append("//input: %s:%s\n"%(
                instance["port_name"], 
                evaluate_parameter(instance["port_size"], instance)))
        elif instance["component"]["name"] == "output":
            output_ports[instance["port_name"]] = instance["port_size"]
            vhdl.append("//output: %s:%s\n"%(
                instance["port_name"], 
                evaluate_parameter(instance["port_size"], instance)))

    ports = []
    port_names = []
    if input_ports or output_ports:
        ports.append("  input clk;")
        ports.append("  input rst;")
        port_names.append("clk")
        port_names.append("rst")


    #Add a top level port for all device outputs and device inputs
    for instance_name, instance in netlist.iteritems():
        for local_name, pin_data in instance["component"]["device_inputs"].iteritems():
            bus, pin_name, size = pin_data
            size = int(evaluate_parameter(size, instance))
            pin_name = str(evaluate_parameter(pin_name, instance))
            vhdl.append('//device_in: %s: %s : "%s" : %s\n'%(bus, pin_name, pin_name, size))
            port_names.append(pin_name)
            if bus == "BIT":
                ports.append("  input %s;"%(pin_name))
            else:
                ports.append("  input [%s : 0] %s;"%(size-1, pin_name))

        for local_name, pin_data in instance["component"]["device_outputs"].iteritems():
            bus, pin_name, size = pin_data
            size = int(evaluate_parameter(size, instance))
            pin_name = str(evaluate_parameter(pin_name, instance))
            vhdl.append('//device_out: %s: %s : "%s" : %s\n'%(bus, pin_name, pin_name, size))
            port_names.append(pin_name)
            if bus == "BIT":
                ports.append("  output %s;"%(pin_name))
            else:
                ports.append("  output [%s : 0] %s;"%(size-1, pin_name))

    #Add a top level port for all input ports and output ports
    for inport, size in input_ports.iteritems():
        size = int(size)
        port_names.append(inport)
        port_names.append(inport + "_stb")
        port_names.append(inport + "_ack")
        ports.append("  input  [%s : 0] %s;"%(size-1, inport))
        ports.append("  input  %s_stb;"%inport)
        ports.append("  output %s_ack;"%inport)

    for outport, size in output_ports.iteritems():
        size = int(size)
        port_names.append(outport)
        port_names.append(outport + "_stb")
        port_names.append(outport + "_ack")
        ports.append("  output [%s : 0] %s;"%(size-1, outport))
        ports.append("  output %s_stb;"%outport)
        ports.append("  input  %s_ack;"%outport)

    return port_names, ports, input_ports, output_ports

def evaluate_parameter(parameter, instance):
    environment = {
        "instance":instance["name"],
        "component":instance["component"]["name"],
    }

    for parameter_name, value in instance["parameters"].iteritems():
        print instance["component"]["name"]
        print value
        environment[parameter_name] = eval(value, environment)

    for name, size in instance["component"]["inputs"].iteritems():
        environment[name] = {}
        environment[name]["bits"] = eval(size, environment)

    for name, size in instance["component"]["inputs"].iteritems():
        environment[name] = {}
        environment[name]["bits"] = eval(size, environment)

    print parameter
    value = eval(parameter, environment)
    return value

def update_size(netlist, instance, wires):
    driver_instance, driver_port = get_input_driver(instance["name"], "in1", wires)
    driver_instance = netlist[driver_instance]
    if driver_instance["component"]["name"] in ["tee", "bend"]:
        update_size(netlist, driver_instance, wires)
    size = driver_instance["component"]["outputs"][driver_port]
    size = evaluate_parameter(size, driver_instance)
    instance["parameters"]["bits"] = str(size)

def get_input_driver(instance_name, port_name, wires):
    for from_instance, from_port, to_instance, to_port in wires:
        if to_instance == instance_name:
            return from_instance, from_port

def update_tees_and_bends(netlist, wires):
    for instance_name, instance in netlist.iteritems():
        if instance["component"]["name"] in ["tee", "bend"]:
            update_size(netlist, instance, wires)


def generate_signals(netlist, input_ports, output_ports, wires, vhdl):

    wire = 0
    for from_instance, from_port, to_instance, to_port in wires:
        from_size = netlist[from_instance]["component"]["outputs"][from_port]
        from_size = int(evaluate_parameter(from_size, netlist[from_instance]))
        to_size = netlist[to_instance]["component"]["inputs"][to_port]
        to_size = int(evaluate_parameter(to_size, netlist[to_instance]))
        if from_size != to_size:
            raise SchematicError("type mismatch:\n from %s_%s port %s is %s to %s_%s port %s is %s"%(
                netlist[from_instance]["component"]["name"], from_instance, from_port, from_size,
                netlist[to_instance]["component"]["name"], to_instance, to_port, to_size))
        if from_size == 1:
            vhdl.append("  wire signal_%s : std_logic;\n"%wire)
        else:
            vhdl.append("  wire signal_%s [%s : 0];\n"%(wire, from_size-1))
        vhdl.append("  wire signal_%s_stb;\n"%wire)
        vhdl.append("  wire signal_%s_ack;\n"%wire)
        wire += 1

    if not(input_ports or output_ports):
        vhdl.append("  wire clk;\n")
        vhdl.append("  wire rst;\n")

def calculate_widths(netlist, wires):
    
    sizes = {}
    for instance_name, instance in netlist:
        component = instance["component"]
        if "size" in component:
            sizes[component["name"]]=component["size"]

    for from_instance, from_port, to_instance, to_port in wires:
        from_instance["component"]["name"] + "." + from_port


def generate(window, component):

    """Make a VHDL component from a schematic"""

    try:
        #Read in the project file
        filename = os.path.join(
            window.project_path.GetValue(),
            component["source_file"])
        open_file = open(filename, 'r')
        sn = pickle.load(open_file)
        netlist = pickle.load(open_file)
        port_positions = pickle.load(open_file)
        wires = pickle.load(open_file)
        documentation = pickle.load(open_file)
        name = os.path.basename(filename).split(".")[0]
        vhdl = []

        update_tees_and_bends(netlist, wires)
        port_names, ports, input_ports, output_ports = generate_ports(netlist, wires, vhdl)
        vhdl.append("//name: %s\n"%name)
        vhdl.append("//source_file: %s\n"%(name+".sch"))
        vhdl.append("module %s (\n    "%name)
        vhdl.append(",\n    ".join(port_names))
        vhdl.append("\n);\n\n")
        vhdl.append("\n".join(ports))
        vhdl.append("\n\n")
        generate_signals(netlist, input_ports, output_ports, wires, vhdl)
        vhdl.append("\n")
        if not (input_ports or output_ports):
            vhdl.append("  \ninitial\n")
            vhdl.append("  begin\n")
            vhdl.append("    rst <= 1'b1;\n")
            vhdl.append("    #50 rst <= 1'b0;\n")
            vhdl.append("  end\n\n")
            vhdl.append("  \ninitial\n")
            vhdl.append("  begin\n")
            vhdl.append("    clk <= 1'b0;\n")
            vhdl.append("    while (1) begin\n")
            vhdl.append("      #5 clk <= ~clk;\n")
            vhdl.append("    end\n")
            vhdl.append("  end\n\n")

        for instance_name, instance in netlist.iteritems():
            if instance["component"]["name"] in ["input", "output"]:
                continue

            generics = []
            for parameter, value in instance["parameters"].iteritems():
                value = evaluate_parameter(value, instance)
                try:
                    generics.append("    .%s (%s)"%(parameter, int(value)))
                except ValueError:
                    generics.append('    .%s ("%s")'%(parameter, str(value)))

            vhdl.append("  %s %s_%s\n"%(
                instance["component"]["name"],
                instance["component"]["name"],
                instance_name, 
                ))

            if generics:
                vhdl.append("  #(\n")
                vhdl.append(",\n".join(generics))
                vhdl.append("\n  )\n")

            signals = []
            wire = 0
            signals.append("    .clk (clk)")
            signals.append("    .rst (rst)")
            for local_name, pin_data in instance["component"]["device_inputs"].iteritems():
                bus, pin_name, size = pin_data
                pin_name = str(evaluate_parameter(pin_name, instance))
                signals.append("    .%s (%s)"%(local_name, pin_name))
            for local_name, pin_data in instance["component"]["device_outputs"].iteritems():
                bus, pin_name, size = pin_data
                pin_name = str(evaluate_parameter(pin_name, instance))
                signals.append("    .%s (%s)"%(local_name, pin_name))
            for from_instance, from_port, to_instance, to_port in wires:
                if from_instance == instance_name:
                    if netlist[to_instance]["component"]["name"] == "output":
                        signals.append("    .%s (%s)"%(
                            from_port,
                            netlist[to_instance]["port_name"]))
                        signals.append("    .%s_stb (%s_stb)"%(
                            from_port,
                            netlist[to_instance]["port_name"]))
                        signals.append("    .%s_ack (%s_ack)"%(
                            from_port,
                            netlist[to_instance]["port_name"]))
                    else:
                        signals.append("    .%s (signal_%s)"%(
                            from_port,
                            wire))
                        signals.append("    .%s_stb (signal_%s_stb)"%(
                            from_port,
                            wire))
                        signals.append("    .%s_ack (signal_%s_ack)"%(
                            from_port,
                            wire))
                if to_instance == instance_name:
                    if netlist[from_instance]["component"]["name"] == "input":
                        signals.append("    .%s (%s)"%(
                            to_port,
                            netlist[from_instance]["port_name"]))
                        signals.append("    .%s_stb (%s_stb)"%(
                            to_port,
                            netlist[from_instance]["port_name"]))
                        signals.append("    .%s_ack (%s_ack)"%(
                            to_port,
                            netlist[from_instance]["port_name"]))
                    else:
                        signals.append("    .%s (signal_%s)"%(
                            to_port,
                            wire))
                        signals.append("    .%s_stb (signal_%s_stb)"%(
                            to_port,
                            wire))
                        signals.append("    .%s_ack (signal_%s_ack)"%(
                            to_port,
                            wire))
                wire += 1
            vhdl.append("  (\n")
            vhdl.append(",\n".join(signals))
            vhdl.append("\n  );\n\n")
        vhdl.append("endmodule\n")

        output_file = os.path.join(window.project_path.GetValue(), name + ".v")
        output_file = open(output_file, "w")
        output_file.write("".join(vhdl))
        output_file.close()
    except SchematicError as err:
        window.transcript.log(err.message)
    window.update()
