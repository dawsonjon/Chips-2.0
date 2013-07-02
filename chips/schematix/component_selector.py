#!/usr/bin/env python
import os
import pickle

import wx
import wx.lib.filebrowsebutton as filebrowse

import docwin
import editor
import c_actions
import schematic_actions
import wxiverilog
import transcript_window

system_components = os.path.join(os.path.dirname(__file__), "..", "toolbox")

class ComponentReadError(Exception):
    def __init__(self, msg):
        self.msg = msg

def edit(window, component):

    """Edit a component"""

    editor.open_file(window.get_component_path(component))
    window.transcript.log("Launching Text Editor")
    window.update()

def delete(window, component):

    """Delete both source and destination"""

    if "source_file" in component:
        if component["source_file"] == "built_in":
            #don't delete builtins
            return
        window.transcript.log("Removing Source File")
        os.remove(window.get_source_path(component))
    window.transcript.log("Removing Component")
    os.remove(window.get_component_path(component))
    window.update()

def parse_vhdl(filename):

    """Extract key facts about the component"""

    component = {
        "name": "",
        "meta_tags": [],
        "inputs": {},
        "outputs": {},
        "dependencies": [],
        "device_inputs": {},
        "device_outputs": {},
        "parameters": {},
        "documentation" : "",
        "file" : os.path.basename(filename),
    }

    VHDL_file = open(filename)
    for line in VHDL_file:
        if line.startswith("---") or line.startswith("///"):
            component["documentation"] += line[3:]
        elif line.startswith("--name") or line.startswith("//name"):
            try:
                component["name"]=line.split(":")[1].strip()
            except IndexError:
                raise ComponentReadError("%s:\nCould not read component name"%filename)
        elif line.startswith("--input") or line.startswith("//input"):
            try:
                component["inputs"][line.split(":")[1].strip()]=line.split(":")[2].strip()
            except IndexError:
                raise ComponentReadError("%s:\nCould not read component input"%filename)
        elif line.startswith("--output") or line.startswith("//output"):
            try:
                component["outputs"][line.split(":")[1].strip()]=line.split(":")[2].strip()
            except IndexError:
                raise ComponentReadError("%s:\nCould not read component output"%filename)
        elif line.startswith("--parameter") or line.startswith("//parameter"):
            try:
                component["parameters"][line.split(":")[1].strip()]=line.split(":")[2].strip()
            except IndexError:
                raise ComponentReadError("%s:\nCould not read component parameter"%filename)
        elif line.startswith("--tag") or line.startswith("//tag"):
            try:
                component["meta_tags"].append(line.split(":")[1].strip())
            except IndexError:
                raise ComponentReadError("%s:\nCould not read meta tag"%filename)
        elif line.startswith("--source_file") or line.startswith("//source_file"):
            try:
                component["source_file"]=line.split(":")[1].strip()
            except IndexError:
                raise ComponentReadError("%s:\nCould not read source file"%filename)
        elif line.startswith("--device_in") or line.startswith("//device_in"):
            try:
                discard, bus, local_name, port_name, size  = [i.strip() for i in line.split(":")]
                bus = bus.upper()
                if bus not in ["BIT", "BUS"]:
                    raise ComponentReadError("%s:\nExpected BIT or BUS in device input"%filename)
                component["device_inputs"][local_name] = (bus, port_name, size)
            except ValueError, IndexError:
                raise ComponentReadError("%s:\nCould not read device input"%filename)
        elif line.startswith("--device_out") or line.startswith("//device_out"):
            try:
                discard, bus, local_name, port_name, size  = [i.strip() for i in line.split(":")]
                bus = bus.upper()
                if bus not in ["BIT", "BUS"]:
                    raise ComponentReadError("%s:\nExpected BIT or BUS in device output"%filename)
                component["device_outputs"][local_name] = (bus, port_name, size)
            except ValueError, IndexError:
                raise ComponentReadError("%s:\nCould not read device output"%filename)
        elif line.startswith("--dependency") or line.startswith("//dependency"):
            try:
                component["dependencies"].append(line.split(":")[1].strip())
            except IndexError:
                raise ComponentReadError("%s:\nCould not read dependencies"%filename)

    return component


class Selector(wx.Panel):

    """A Component selection window.
    
    - Provides component selection using a tree widget.
    - Provides context sensitive help.
    
    """

    def __init__(self, parent, *args):

        """Create a component selection window, add available components."""

        #layout window
        wx.Panel.__init__(self, parent, *args)
        self.parent = parent
        horizontal_splitter = wx.SplitterWindow(self)
        self.project_path = filebrowse.DirBrowseButton(
                self, 
                -1,
                labelText="Project Directory",
                startDirectory=os.getcwd(),
        )
        self.project_path.SetValue(os.path.join(os.getcwd(), "components"))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.project_path, 0, wx.EXPAND)
        sizer.Add(horizontal_splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

        #Create Component Browser
        vertical_splitter = wx.SplitterWindow(horizontal_splitter)
        panel = wx.Panel(vertical_splitter, -1)
        self.selector = wx.TreeCtrl(
                panel, 
                style=wx.SUNKEN_BORDER|wx.TR_DEFAULT_STYLE
        )
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(panel, -1, "Component Browser"), 0, wx.EXPAND)
        sizer.Add(self.selector, 1, wx.EXPAND)
        panel.SetSizer(sizer)

        #Create Document Window
        dw = wx.Panel(vertical_splitter, -1)
        self.document_window = docwin.DocWin(dw, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(dw, -1, "Documentation"), 0, wx.EXPAND)
        sizer.Add(self.document_window, 1, wx.EXPAND)
        dw.SetSizer(sizer)

        vertical_splitter.SplitVertically(panel, dw, 0)

        #Create transcript window
        tw = wx.Panel(horizontal_splitter, -1)
        self.transcript = transcript_window.TranscriptWindow(tw)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(tw, -1, "Transcript"), 0, wx.EXPAND)
        sizer.Add(self.transcript, 1, wx.EXPAND)
        tw.SetSizer(sizer)
        horizontal_splitter.SplitHorizontally(vertical_splitter, tw, -200)

        #Bind Events
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_select_item, self.selector)
        parent.Bind(wx.EVT_CLOSE, lambda evt: self.on_exit())
        parent.Bind(wx.EVT_ACTIVATE, lambda evt: self.update())
        self.selector.Bind(wx.EVT_RIGHT_DOWN, self.on_right_click_item)
        self.selector.Bind(wx.EVT_LEFT_DCLICK, self.on_left_dclick_item)

        #initialise component browser
        self.selector.DeleteAllItems()
        root = self.selector.AddRoot("Component Categories")
        self.tags = {}
        self.tag_components = {}
        self.schematic_windows = {}
        self.update()
        self.selector.ExpandAll()

    def on_exit(self):
        for window in self.schematic_windows.values():
            window.Close()
        self.parent.Destroy()

    def update(self):

        """Update the component selector tree after a change"""

        library = {"uncategorised":[]}
        for directory in (system_components, self.project_path.GetValue()):
            for component in os.listdir(directory):
                if (component.endswith(".vhd") or
                    component.endswith(".vhdl") or
                    component.endswith(".v")):
                    filename = os.path.join(directory, component)
                    try:
                        component = parse_vhdl(filename)
                    except ComponentReadError as err:
                        self.transcript.log("Error reading file %s"%filename)
                        self.transcript.log(err.msg)
                        continue
                    if "meta_tags" in component and component["meta_tags"]:
                        for tag in component["meta_tags"]:
                            if tag in library:
                                library[tag].append(component)
                            else:
                                library[tag] = [component]
                    else:
                        library["uncategorised"].append(component)

        #delete non-existent tags and components
        delete_tags = []
        for tag in self.tags:
            if tag not in library:
                self.selector.Delete(self.tags[tag])
                delete_tags.append(tag)

        for tag in delete_tags:
            self.tags.pop(tag)
            self.tag_components.pop(tag)

        delete_components = []
        for tag, tag_components in self.tag_components.iteritems():
            for title, node in tag_components.iteritems():
                library_titles = []
                for c in library[tag]:
                    library_titles.append(c["name"])
                if title not in library_titles:
                    self.selector.Delete(node)
                    delete_components.append((tag, title))

        for tag, title in delete_components:
            self.tag_components[tag].pop(title)

        #add newly created tags
        for tag, tag_components in library.iteritems():
            if tag not in self.tags:
                tag_node = self.selector.AppendItem(self.selector.GetRootItem(), tag)
                self.tags[tag] = tag_node
                self.tag_components[tag] = {}
            for component in tag_components:
                title = component["name"]
                if title not in self.tag_components[tag]:
                    node = self.selector.AppendItem(self.tags[tag], title)
                    self.tag_components[tag][title] = node
                    self.selector.SetItemPyData(node, component)

        #Update components
        for tag, components in library.iteritems():
            for component in components:
                node = self.tag_components[tag][component["name"]]
                self.selector.SetItemPyData(node, component)
                if not self.is_up_to_date(component):
                    self.selector.SetItemTextColour(node, "red")
                else:
                    self.selector.SetItemTextColour(node, "black")

        for schematic in self.schematic_windows.values():
            schematic.draw()

    def on_select_item(self, event):

        """When a new component is selected, update the help window."""

        component = self.selector.GetSelection()
        self.component = self.selector.GetItemPyData(component)
        if self.component is not None and "documentation" in self.component and self.component["documentation"]:
            self.document_window.set_RsT(self.component["documentation"])
        else:
            self.document_window.set_RsT("*No Documentation Available*")

    def new_instance(self):

        """Return a dictionary describing the component"""

        self.transcript.log("Creating Component Instance")
        component = self.selector.GetSelection()
        component = self.selector.GetItemPyData(component)
        if "name" in component:
            return component
        else:
            return None

    def on_left_dclick_item(self, event):

        """Edit the source if applicable"""

        pt = event.GetPosition();
        component, flags = self.selector.HitTest(pt)
        component = self.selector.GetItemPyData(component)

        if component is not None:
            if "source_file" in component:
                if component["source_file"].endswith(".sch"):
                    schematic_actions.edit(self, component),
                elif component["source_file"].endswith(".c"):
                    c_actions.edit(self, component),

    def on_right_click_item(self, event):

        """Show a context menu for the schematic"""

        pt = event.GetPosition();
        component, flags = self.selector.HitTest(pt)
        component = self.selector.GetItemPyData(component)
        menu = wx.Menu()

        if component is None:
            self.Bind(wx.EVT_MENU, 
                lambda evt: c_actions.new(self),
                menu.Append(-1, "New C file"),
            )
            self.Bind(wx.EVT_MENU, 
                lambda evt: schematic_actions.new(self),
                menu.Append(-1, "New Schematic"),
            )
        else:
            if "source_file" in component:
                self.Bind(wx.EVT_MENU, 
                    lambda evt: delete(self, component),
                    menu.Append(-1, "Delete"),
                )
                if component["source_file"].endswith(".sch"):
                    self.Bind(wx.EVT_MENU, 
                        lambda evt: schematic_actions.edit(self, component),
                        menu.Append(-1, "Edit"),
                    )
                    if not self.is_up_to_date(component):
                        self.Bind(wx.EVT_MENU, 
                            lambda evt: schematic_actions.generate(self, component),
                            menu.Append(-1, "Generate"),
                        )
                elif component["source_file"].endswith(".c"):
                    self.Bind(wx.EVT_MENU, 
                        lambda evt: c_actions.edit(self, component),
                        menu.Append(-1, "Edit"),
                    )
                    if not self.is_up_to_date(component):
                        self.Bind(wx.EVT_MENU, 
                            lambda evt: c_actions.generate(self, component),
                            menu.Append(-1, "Generate"),
                        )
            if "file" in component:
                self.Bind(wx.EVT_MENU, 
                    lambda evt: edit(self, component),
                    menu.Append(-1, "View Component"),
                )
                self.Bind(wx.EVT_MENU, 
                    lambda evt: self.simulate(component),
                    menu.Append(-1, "Icarus Verilog Simulation"),
                )

        self.PopupMenu(menu)

    def get_component_path(self, component):

        """Get the file path of a component"""

        if component["source_file"] == "built_in":
            return os.path.join(system_components, component["file"])
        else:
            return os.path.join(self.project_path.GetValue(), component["file"])

    def get_source_path(self, component):

        """Get the source file path of a component"""

        return os.path.join(self.project_path.GetValue(), component["source_file"])

    def get_component_named(self, name):

        """Return the component with the given name"""

        for directory in (system_components, self.project_path.GetValue()):
            for component in os.listdir(directory):
                if (component.endswith(".vhd") or 
                    component.endswith(".vhdl") or 
                    component.endswith(".v")):
                    filename = os.path.join(directory, component)
                    component = parse_vhdl(filename)
                    if component["name"]==name:
                        return component
        return None

    def get_dependencies(self, component):

        """Return a list including the component, and all the components it depends on"""

        #Accessing the component by name forces the generated component to be parsed
        component = self.get_component_named(component["name"])
        dependencies = []
        for i in component["dependencies"]:
            dependencies.extend(self.get_dependencies(self.get_component_named(i)))

        return dependencies + [component]

    def generate_dependencies(self, component):

        """Generate from source all dependencies"""
        
        for dependency in self.get_dependencies(component):
            if not self.is_up_to_date(dependency):
                if "source_file" in dependency and dependency["source_file"] not in ["built_in"]:
                    if dependency["source_file"].endswith(".c"):
                        c_actions.generate(self, dependency)
                    elif dependency["source_file"].endswith(".sch"):
                        schematic_actions.generate(self, dependency)

    def simulate(self, component):

        """Simulate component"""

        self.transcript.log("Generating all dependencies")
        self.generate_dependencies(component)
        self.transcript.log("Creating file list")
        file_list = []
        for dependency in self.get_dependencies(component):
            file_list.append(self.get_component_path(dependency))
        self.transcript.log("Launching Verilog simulator")
        wxiverilog.VerilogProject(file_list, component["name"])


    def is_up_to_date(self, component):

        """Determines whether a file needs to be regenerated"""

        if "source_file" not in component:
            return True

        if component["source_file"] == "built_in":
            return True

        source_path = os.path.join(
          self.project_path.GetValue(),
          component["source_file"]
        )

        dest_path = os.path.join(
          self.project_path.GetValue(),
          component["file"]
        )

        source_updated = os.path.getmtime(source_path)
        dest_updated = os.path.getmtime(dest_path)

        return source_updated < dest_updated
