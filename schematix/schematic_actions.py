#!/usr/bin/env python
import os
import pickle

import wx

import schematix

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

def generate_ports(netlist, vhdl):

    """Generate a list of ports and device io."""

    input_ports = []
    output_ports = []
    for instance_name, instance in netlist.iteritems():
        if instance["component"]["name"] == "input":
            input_ports.append(instance["port_name"])
            vhdl.append("--input: %s\n"%instance["port_name"])
        elif instance["component"]["name"] == "output":
            output_ports.append(instance["port_name"])
            vhdl.append("--output: %s\n"%instance["port_name"])

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

    for inport in input_ports:
        ports.append("    %s : in std_logic_vector(15 downto 0)"%inport)
        ports.append("    %s_STB : in std_logic"%inport)
        ports.append("    %s_ACK : out std_logic"%inport)

    for outport in output_ports:
        ports.append("    %s : out std_logic_vector(15 downto 0)"%outport)
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
            size = int(size)
            if size == 1:
                ports.append("    %s : in std_logic"%pin_name)
            else:
                ports.append("    %s : in std_logic_vector(%s downto 0)"%(pin_name, size-1))

        for pin_name, size in instance["component"]["device_outputs"].iteritems():
            size = int(size)
            if size == 1:
                ports.append("    %s : out std_logic"%pin_name)
            else:
                ports.append("    %s : out std_logic_vector(%s downto 0)"%(pin_name, size-1))

        for inport in instance["component"]["inputs"]:
            ports.append("    %s : in std_logic_vector(15 downto 0)"%inport)
            ports.append("    %s_STB : in std_logic"%inport)
            ports.append("    %s_ACK : out std_logic"%inport)

        for outport in instance["component"]["outputs"]:
            ports.append("    %s : out std_logic_vector(15 downto 0)"%outport)
            ports.append("    %s_STB : out std_logic"%outport)
            ports.append("    %s_ACK : in std_logic"%outport)

        if ports:
            vhdl.append("    port(\n")
            vhdl.append(";\n".join(ports))
            vhdl.append("\n  );\n")
        vhdl.append("  end component %s;\n\n"%instance["component"]["name"])

def generate_signals(input_ports, output_ports, wires, vhdl):

    wire = 0
    for from_instance, from_port, to_instance, to_port in wires:
        vhdl.append("  signal signal_%s : std_logic_vector(15 downto 0);\n"%wire)
        vhdl.append("  signal signal_%s_STB : std_logic;\n"%wire)
        vhdl.append("  signal signal_%s_ACK : std_logic;\n"%wire)
        wire += 1

    if not(input_ports or output_ports):
        vhdl.append("  signal CLK : std_logic;\n")
        vhdl.append("  signal RST : std_logic;\n")

def generate(window, component):

    """Make a VHDL component from a schematic"""

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

    ports, input_ports, output_ports = generate_ports(netlist, vhdl)
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
    generate_signals(input_ports, output_ports, wires, vhdl)
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
    window.update()
