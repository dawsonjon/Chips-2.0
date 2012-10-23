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

    schematic = schematix.BlockFrame(window, None, size=(1024,768), title="Schematix")
    schematic.Show()
    schematic.open(window.get_source_path(component))
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
        new_file = name + ".vhd"
        new_file = os.path.join(
            window.project_path.GetValue(),
            new_file)
        new_file = open(new_file, "w")
        new_file.write("--name : %s\n"%name)
        new_file.write("--source_file : %s\n"%(name+".sch"))
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
        new_file.close()
        window.update()

def generate_ports(netlist, wires, vhdl):

    """Generate a list of ports and device io."""

    input_ports = {}
    output_ports = {}
    for instance_name, instance in netlist.iteritems():
        if instance["component"]["name"] == "input":
            input_ports[instance["port_name"]] = instance["port_size"]
            vhdl.append("--input: %s:%s\n"%(instance["port_name"], instance["port_size"]))
        elif instance["component"]["name"] == "output":
            output_ports[instance["port_name"]] = instance["port_size"]
            vhdl.append("--output: %s:%s\n"%(instance["port_name"], instance["port_size"]))

    ports = []
    if input_ports or output_ports:
        ports.append("    CLK : in std_logic")
        ports.append("    RST : in std_logic")

    for instance_name, instance in netlist.iteritems():
        for pin_name, size in instance["component"]["device_inputs"].iteritems():
            size = int(size)
            vhdl.append("--device_in: %s_%s : %s\n"%(instance_name, pin_name, size))
            if size == 1:
                ports.append("    %s_%s : in std_logic"%(instance_name, pin_name))
            else:
                ports.append("    %s_%s : in std_logic_vector(%s downto 0)"%(instance_name, pin_name, size-1))

        for pin_name, size in instance["component"]["device_outputs"].iteritems():
            size = int(size)
            vhdl.append("--device_out: %s_%s : %s\n"%(instance_name, pin_name, size))
            if size == 1:
                ports.append("    %s_%s : out std_logic"%(instance_name, pin_name))
            else:
                ports.append("    %s_%s : out std_logic_vector(%s downto 0)"%(instance_name, pin_name, size-1))

    for inport, size in input_ports.iteritems():
        size = int(size)
        if size == 1:
            ports.append("    %s : in std_logic"%(inport, size-1))
        else:
            ports.append("    %s : in std_logic_vector(%s downto 0)"%(inport, size-1))
        ports.append("    %s_STB : in std_logic"%inport)
        ports.append("    %s_ACK : out std_logic"%inport)

    for outport, size in output_ports.iteritems():
        size = int(size)
        if size == 1:
            ports.append("    %s : out std_logic"%(outport, size-1))
        else:
            ports.append("    %s : out std_logic_vector(%s downto 0)"%(outport, size-1))
        ports.append("    %s_STB : out std_logic"%outport)
        ports.append("    %s_ACK : in std_logic"%outport)

    return ports, input_ports, output_ports


def generate_components(netlist, vhdl):

    components = []
    for instance_name, instance in netlist.iteritems():
        if instance["component"]["name"] in components:
            continue
        if instance["component"]["name"] in ["input", "output"]:
            continue
        vhdl.append("--dependency: %s\n"%instance["component"]["name"])
        components.append(instance["component"]["name"])
        vhdl.append("  component %s is\n"%instance["component"]["name"])

        generics = []
        for parameter, default in instance["component"]["parameters"].iteritems():
            generics.append("    %s : integer := %s"%(parameter, default))

        if generics:
            vhdl.append("    generic(\n")
            vhdl.append(";\n".join(generics))
            vhdl.append("    );\n")

        ports = []
        ports.append("    CLK : in std_logic")
        ports.append("    RST : in std_logic")

        for pin_name, size in instance["component"]["device_inputs"].iteritems():
            ports.append("    %s : in std_logic_vector(%s-1 downto 0)"%(pin_name, size))

        for pin_name, size in instance["component"]["device_outputs"].iteritems():
            ports.append("    %s : out std_logic_vector(%s-1 downto 0)"%(pin_name, size))

        for inport, size in instance["component"]["inputs"].iteritems():
            ports.append("    %s : in std_logic_vector(%s-1 downto 0)"%(inport, size))
            ports.append("    %s_STB : in std_logic"%inport)
            ports.append("    %s_ACK : out std_logic"%inport)

        for outport, size in instance["component"]["outputs"].iteritems():
            ports.append("    %s : out std_logic_vector(%s-1 downto 0)"%(outport, size))
            ports.append("    %s_STB : out std_logic"%outport)
            ports.append("    %s_ACK : in std_logic"%outport)

        if ports:
            vhdl.append("    port(\n")
            vhdl.append(";\n".join(ports))
            vhdl.append("\n  );\n")
        vhdl.append("  end component %s;\n\n"%instance["component"]["name"])

def parse_size(size, instance):

    """Get an integer value of size, size may be an instance parameter"""

    if size in instance["parameters"]:
        return parse_size(instance["parameters"][size], instance)
    else:
        return int(size)

def update_tees_and_bends(netlist, wires):

    """For convenience, tees and bends assume the type of the thing that drives them"""

    for instance_name, instance in netlist.iteritems():
        if instance["component"]["name"] in ["tee", "bend"]:
            #find the source of the driving signal
            for from_instance, from_port, to_instance, to_port in wires:
                if to_instance == instance_name:
                    size = netlist[from_instance]["component"]["outputs"][from_port]
                    size = parse_size(size, netlist[from_instance])
                    instance["parameters"]["bits"] = size


def generate_signals(netlist, input_ports, output_ports, wires, vhdl):

    wire = 0
    for from_instance, from_port, to_instance, to_port in wires:
        from_size = netlist[from_instance]["component"]["outputs"][from_port]
        from_size = parse_size(from_size, netlist[from_instance])
        to_size = netlist[to_instance]["component"]["inputs"][to_port]
        to_size = parse_size(to_size, netlist[to_instance])
        if from_size != to_size:
            raise SchematicError("type mismatch:\n from %s_%s port %s is %s to %s_%s port %s is %s"%(
                netlist[from_instance]["component"]["name"], from_instance, from_port, from_size,
                netlist[to_instance]["component"]["name"], to_instance, to_port, to_size))
        if from_size == 1:
            vhdl.append("  signal signal_%s : std_logic;\n"%wire)
        else:
            vhdl.append("  signal signal_%s : std_logic_vector(%s downto 0);\n"%(wire, from_size-1))
        vhdl.append("  signal signal_%s_STB : std_logic;\n"%wire)
        vhdl.append("  signal signal_%s_ACK : std_logic;\n"%wire)
        wire += 1

    if not(input_ports or output_ports):
        vhdl.append("  signal CLK : std_logic;\n")
        vhdl.append("  signal RST : std_logic;\n")

def calculate_widths(netslit, wires):
    
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
        name = os.path.basename(filename).split(".")[0]
        vhdl = []

        update_tees_and_bends(netlist, wires)
        ports, input_ports, output_ports = generate_ports(netlist, wires, vhdl)
        vhdl.append("--name: %s\n"%name)
        vhdl.append("--source_file: %s\n"%(name+".sch"))
        vhdl.append("library ieee;\n")
        vhdl.append("use ieee.std_logic_1164.all;\n")
        vhdl.append("use ieee.numeric_std.all;\n\n")
        vhdl.append("entity %s is\n"%name)
        if ports:
            vhdl.append("  port(\n")
            vhdl.append(";\n".join(ports))
            vhdl.append("  );\n")
        vhdl.append("end entity %s;\n\n"%name)
        vhdl.append("architecture RTL of %s is\n\n"%name)
        generate_components(netlist, vhdl)
        generate_signals(netlist, input_ports, output_ports, wires, vhdl)
        vhdl.append("begin\n\n")
        if not (input_ports or output_ports):
            vhdl.append("  GENERATE_CLK : process\n")
            vhdl.append("  begin\n")
            vhdl.append("    while True loop\n")
            vhdl.append("      CLK <= '0';\n")
            vhdl.append("      wait for 5 ns;\n")
            vhdl.append("      CLK <= '1';\n")
            vhdl.append("      wait for 5 ns;\n")
            vhdl.append("    end loop;\n")
            vhdl.append("    wait;\n")
            vhdl.append("  end process GENERATE_CLK;\n\n")

            vhdl.append("  GENERATE_RST : process\n")
            vhdl.append("  begin\n")
            vhdl.append("    RST <= '1';\n")
            vhdl.append("    wait for 50 ns;\n")
            vhdl.append("    RST <= '0';\n")
            vhdl.append("    wait;\n")
            vhdl.append("  end process GENERATE_RST;\n\n")

        for instance_name, instance in netlist.iteritems():
            if instance["component"]["name"] in ["input", "output"]:
                continue

            generics = []
            for parameter, value in instance["parameters"].iteritems():
                generics.append("    %s => %s"%(parameter, value))

            vhdl.append("  %s_%s : %s\n"%(
                instance["component"]["name"],
                instance_name, 
                instance["component"]["name"]))
            if generics:
                vhdl.append("  generic map(\n")
                vhdl.append(",\n".join(generics))
                vhdl.append("\n  )\n")

            vhdl.append("  port map (\n")
            signals = []
            wire = 0
            signals.append("    CLK => CLK")
            signals.append("    RST => RST")
            for pin_name, size in instance["component"]["device_inputs"].iteritems():
                signals.append("    %s => %s_%s"%(pin_name, instance_name, pin_name))
            for pin_name, size in instance["component"]["device_outputs"].iteritems():
                signals.append("    %s => %s_%s"%(pin_name, instance_name, pin_name))
            for from_instance, from_port, to_instance, to_port in wires:
                if from_instance == instance_name:
                    if netlist[to_instance]["component"]["name"] == "output":
                        signals.append("    %s => %s"%(
                            from_port,
                            netlist[to_instance]["port_name"]))
                        signals.append("    %s_STB => %s_STB"%(
                            from_port,
                            netlist[to_instance]["port_name"]))
                        signals.append("    %s_ACK => %s_ACK"%(
                            from_port,
                            netlist[to_instance]["port_name"]))
                    else:
                        signals.append("    %s => signal_%s"%(
                            from_port,
                            wire))
                        signals.append("    %s_STB => signal_%s_STB"%(
                            from_port,
                            wire))
                        signals.append("    %s_ACK => signal_%s_ACK"%(
                            from_port,
                            wire))
                if to_instance == instance_name:
                    if netlist[from_instance]["component"]["name"] == "input":
                        signals.append("    %s => %s"%(
                            to_port,
                            netlist[from_instance]["port_name"]))
                        signals.append("    %s_STB => %s_STB"%(
                            to_port,
                            netlist[from_instance]["port_name"]))
                        signals.append("    %s_ACK => %s_ACK"%(
                            to_port,
                            netlist[from_instance]["port_name"]))
                    else:
                        signals.append("    %s => signal_%s"%(
                            to_port,
                            wire))
                        signals.append("    %s_STB => signal_%s_STB"%(
                            to_port,
                            wire))
                        signals.append("    %s_ACK => signal_%s_ACK"%(
                            to_port,
                            wire))
                wire += 1
            vhdl.append(",\n".join(signals))
            vhdl.append("\n  );\n\n")
        vhdl.append("end architecture RTL;\n")

        output_file = os.path.join(window.project_path.GetValue(), name + ".vhd")
        output_file = open(output_file, "w")
        output_file.write("".join(vhdl))
        output_file.close()
    except SchematicError as err:
        window.transcript.log(err.message)
    window.update()
