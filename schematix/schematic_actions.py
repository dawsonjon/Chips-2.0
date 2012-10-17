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

def generate(window, component):

    """Make a VHDL component from a schematic"""

    filename = os.path.join(
        window.project_path.GetValue(),
        component["source_file"])

    open_file = open(filename, 'r')
    sn = pickle.load(open_file)
    netlist = pickle.load(open_file)
    port_positions = pickle.load(open_file)
    wires = pickle.load(open_file)

    name = os.path.basename(filename).split(".")[0]
    output_file = os.path.join(window.project_path.GetValue(), name + ".vhd")
    output_file = open(output_file, "w")

    output_file.write("--name: %s\n"%name)
    output_file.write("--source_file: %s\n"%(name+".sch"))

    input_ports = []
    output_ports = []
    for instance_name, instance in netlist.iteritems():
        if instance["component"]["name"] == "input":
            input_ports.append(instance["port_name"])
            output_file.write("--input: %s\n"%instance["port_name"])
        elif instance["component"]["name"] == "output":
            output_ports.append(instance["port_name"])
            output_file.write("--output: %s\n"%instance["port_name"])

    output_file.write("entity %s is\n"%name)
    output_file.write("  port(\n")
    ports = []
    ports.append("    CLK : in std_logic")
    ports.append("    RST : in std_logic")

    for instance_name, instance in netlist.iteritems():
        for pin_name, size in instance["component"]["device_inputs"].iteritems():
            size = int(size)
            output_file.write("--device_in: %s_%s : %s\n"%(instance_name, pin_name, size))
            if size == 1:
                ports.append("    %s_%s : in std_logic"%(instance_name, pin_name))
            else:
                ports.append("    %s_%s : in std_logic_vector(%s downto 0)"%(instance_name, pin_name, size-1))

        for pin_name, size in instance["component"]["device_outputs"].iteritems():
            size = int(size)
            output_file.write("--device_out: %s_%s : %s\n"%(instance_name, pin_name, size))
            if size == 1:
                ports.append("    %s_%s : out std_logic"%(instance_name, pin_name))
            else:
                ports.append("    %s_%s : out std_logic_vector(%s downto 0)"%(instance_name, pin_name, size-1))

    for inport in input_ports:
        ports.append("    %s : in std_logic_vector"%inport)
        ports.append("    %s_STB : in std_logic"%inport)
        ports.append("    %s_ACK : out std_logic"%inport)

    for outport in output_ports:
        output_ports
        ports.append("    %s : out std_logic_vector"%outport)
        ports.append("    %s_STB : out std_logic"%outport)
        ports.append("    %s_ACK : in std_logic"%outport)

    output_file.write(";\n".join(ports))
    output_file.write(");\n")
    output_file.write("end entity %s;\n\n"%name)
    output_file.write("architecture RTL of %s\n\n"%name)
    components = []

    for instance_name, instance in netlist.iteritems():
        if instance["component"]["name"] in components:
            continue
        if instance["component"]["name"] in ["input", "output"]:
            continue
        output_file.write("--dependency: %s\n"%instance["component"]["name"])
        components.append(instance["component"]["name"])
        output_file.write("  component %s is\n"%instance["component"]["name"])
        output_file.write("    generic(\n")
        generics = []
        for parameter, default in instance["component"]["parameters"].iteritems():
            generics.append("    %s : integer := %s"%(parameter, default))
        output_file.write(";\n".join(generics))
        output_file.write("    );\n")
        output_file.write("    port(\n")
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
            ports.append("    %s : in std_logic_vector"%inport)
            ports.append("    %s_STB : in std_logic"%inport)
            ports.append("    %s_ACK : out std_logic"%inport)

        for outport in instance["component"]["outputs"]:
            ports.append("    %s : out std_logic_vector"%outport)
            ports.append("    %s_STB : out std_logic"%outport)
            ports.append("    %s_ACK : in std_logic"%outport)

        output_file.write(";\n".join(ports))
        output_file.write("\n  );\n")
        output_file.write("  end component %s;\n\n"%instance["component"]["name"])

    wire = 0
    for from_instance, from_port, to_instance, to_port in wires:
        output_file.write("  signal signal_%s : std_logic_vector(15 downto 0);\n"%wire)
        wire += 1
    output_file.write("begin\n\n")
    for instance_name, instance in netlist.iteritems():
        if instance["component"]["name"] in ["input", "output"]:
            continue
        output_file.write("  %s : %s generic map(\n"%(
            instance_name, instance["component"]["name"]))
        generics = []
        for parameter, value in instance["parameters"].iteritems():
            generics.append("    %s => %s"%(parameter, value))
        output_file.write(",\n".join(generics))
        output_file.write("\n  ) port map (\n")
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
        output_file.write(",\n".join(signals))
        output_file.write("\n  );\n")
    output_file.write("end architecture RTL;\n")
    output_file.close()
    window.update()
