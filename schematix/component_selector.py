#!/usr/bin/env python
import os
import pickle

import wx
import wx.lib.filebrowsebutton as filebrowse

import docwin
import editor
import c_actions
import schematic_actions

system_components = os.path.join(os.path.dirname(__file__), "system_components")

def edit(window, component):

    """Edit a component"""

    editor.open_file(window.get_component_path(component))
    window.update()

def delete(window, component):

    """Delete both source and destination"""

    if "source_file" in component:
        if component["source_file"] == "built_in":
            #don't delete builtins
            return
        os.remove(window.get_source_path(component))
    os.remove(window.get_component_path(component))
    window.update()

def new(window):

    """Make a new component"""

    dlg = wx.TextEntryDialog(
        window, 
        "Component name:",
        "New Component")
    if dlg.ShowModal() == wx.ID_OK:
        name = dlg.GetValue()
        new_file = name + ".vhd"
        new_file = os.path.join(
            window.project_path.GetValue(),
            new_file)
        new_file = os.path.join(window.project, new_file)
        new_file = open(new_file, "w")
        new_file.write("--name : %s\n"%name)
        new_file.close()
        window.update()

def parse_vhdl(filename):

    """Extract key facts about the component"""

    component = {
        "name": "",
        "meta_tags": [],
        "inputs": [],
        "outputs": [],
        "device_inputs": {},
        "device_outputs": {},
        "parameters": {},
        "documentation" : "",
        "file" : os.path.basename(filename),
    }

    VHDL_file = open(filename)
    for line in VHDL_file:
        if line.startswith("---"):
            component["documentation"] += line[3:]
        elif line.startswith("--name"):
            component["name"]=line.split(":")[1].strip()
        elif line.startswith("--input"):
            component["inputs"].append(line.split(":")[1].strip())
        elif line.startswith("--output"):
            component["outputs"].append(line.split(":")[1].strip())
        elif line.startswith("--parameter"):
            component["parameters"][line.split(":")[1].strip()] = line.split(":")[2].strip()
        elif line.startswith("--tag"):
            component["meta_tags"].append(line.split(":")[1].strip())
        elif line.startswith("--source_file"):
            component["source_file"]=line.split(":")[1].strip()
        elif line.startswith("--device_in"):
            component["device_inputs"][line.split(":")[1].strip()] = line.split(":")[2].strip()
        elif line.startswith("--device_out"):
            component["device_outputs"][line.split(":")[1].strip()] = line.split(":")[2].strip()

    return component


class Selector(wx.SplitterWindow):

    """A Component selection window.
    
    - Provides component selection using a tree widget.
    - Provides context sensitive help.
    
    """

    def __init__(self, parent, *args):

        """Create a component selection window, add available components."""

        wx.SplitterWindow.__init__(self, parent, *args)

        panel = wx.Panel(self, -1)
        self.project_path = filebrowse.DirBrowseButton(
                panel, 
                -1,
                labelText="Project Directory",
                startDirectory=os.getcwd(),
        )
        self.project_path.SetValue(os.path.join(os.getcwd(), "components"))
        self.selector = wx.TreeCtrl(
                panel, 
                style=wx.SUNKEN_BORDER|wx.TR_DEFAULT_STYLE
        )
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.project_path, 0, wx.EXPAND)
        sizer.Add(self.selector, 1, wx.EXPAND)
        panel.SetSizer(sizer)

        self.document_window = docwin.DocWin(self, -1)
        self.SplitHorizontally(panel, self.document_window, 0)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_select_item, self.selector)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.on_right_click_item, self.selector)

        self.selector.DeleteAllItems()
        root = self.selector.AddRoot("Component Categories")
        self.tags = {}
        self.tag_components = {}
        self.update()

    def update(self):

        """Update the component selector tree after a change"""

        library = {"all":[]}
        for directory in (system_components, self.project_path.GetValue()):
            for component in os.listdir(directory):
                if component.endswith(".vhd"):
                    filename = os.path.join(directory, component)
                    component = parse_vhdl(filename)
                    if "meta_tags" in component:
                        for tag in component["meta_tags"]:
                            if tag in library:
                                library[tag].append(component)
                            else:
                                library[tag] = [component]
                    library["all"].append(component)

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

        #mark out of date items
        for tag, components in library.iteritems():
            for component in components:
                node = self.tag_components[tag][component["name"]]
                if not self.is_up_to_date(component):
                    self.selector.SetItemTextColour(node, "red")
                else:
                    self.selector.SetItemTextColour(node, "black")

    def on_select_item(self, event):

        """When a new component is selected, update the help window."""

        component = self.selector.GetSelection()
        self.component = self.selector.GetItemPyData(component)
        if self.component is not None and "documentation" in self.component and self.component["documentation"]:
            self.document_window.set_RsT(self.component["documentation"])
        else:
            self.document_window.set_RsT("*No Documentation Available*")

    def new_instance(self):

        """Return a dictionary describing the component."""

        component = self.selector.GetSelection()
        component = self.selector.GetItemPyData(component)
        if "name" in component:
            return component
        else:
            return None

    def on_right_click_item(self, event):

        """Show a context menu for the schematic"""

        component = event.GetItem()
        component = self.selector.GetItemPyData(component)
        menu = wx.Menu()
        self.Bind(wx.EVT_MENU, 
            lambda evt: new(self),
            menu.Append(-1, "New Chip"),
        )
        self.Bind(wx.EVT_MENU, 
            lambda evt: c_actions.new(self),
            menu.Append(-1, "New C file"),
        )
        self.Bind(wx.EVT_MENU, 
            lambda evt: schematic_actions.new(self),
            menu.Append(-1, "New Schematic"),
        )
        if component is not None:
            if "file" in component:
                self.Bind(wx.EVT_MENU, 
                    lambda evt: edit(self, component),
                    menu.Append(-1, "Edit Chip"),
                )
                self.Bind(wx.EVT_MENU, 
                    lambda evt: simulate(self, component),
                    menu.Append(-1, "Simulate Chip"),
                )
            if "source_file" in component:
                self.Bind(wx.EVT_MENU, 
                    lambda evt: delete(self, component),
                    menu.Append(-1, "Delete"),
                )
                if component["source_file"].endswith(".sch"):
                    self.Bind(wx.EVT_MENU, 
                        lambda evt: schematic_actions.edit(self, component),
                        menu.Append(-1, "Edit Schematic"),
                    )
                    if not self.is_up_to_date(component):
                        self.Bind(wx.EVT_MENU, 
                            lambda evt: schematic_actions.generate(self, component),
                            menu.Append(-1, "Generate from Schematic"),
                        )
                elif component["source_file"].endswith(".c"):
                    self.Bind(wx.EVT_MENU, 
                        lambda evt: c_actions.edit(window, component),
                        menu.Append(-1, "Edit C File"),
                    )
                    if not self.is_up_to_date(component):
                        self.Bind(wx.EVT_MENU, 
                            lambda evt: c_actions.generate(window, component),
                            menu.Append(-1, "Generate from C File"),
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
