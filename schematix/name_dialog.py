import wx
from wx.lib.scrolledpanel import ScrolledPanel

class PythonExpValidator(wx.PyValidator):

    """A port name validator
    
    * Tranfers Data to and from windows in a dialog box.
    * Checks that entered data is a valid name
    """

    def __init__(self, instance, names):
        wx.PyValidator.__init__(self)
        self.instance = instance
        self.names = names

    def Clone(self):
        return PythonExpValidator(self.instance, self.names)

    def Validate(self, win):
        textctrl = self.GetWindow()
        text = textctrl.GetValue()
        if text.upper() in [i.upper() for i in self.names]:
            if text != self.instance["port_name"]:
                wx.MessageBox("%s already exists"%text)
                return False

        for char in text:
            if char.isalnum() or char == "_":
                continue
            wx.MessageBox("%s contains invalid characters"%text)
            return False

        if "__" in text:
            wx.MessageBox("%s contains two sequencial '_' characters"%text)
            return False

        if len(text) < 1:
            wx.MessageBox("%s is too short"%text)
            return False

        if not text[0].isalpha():
            wx.MessageBox("%s does not start with an alphabetic character"%text)
            return False

        return True

    def TransferToWindow(self):
        name = self.instance["port_name"]
        self.GetWindow().SetValue(name)
        return True

    def TransferFromWindow(self):
        name = self.GetWindow().GetValue()
        self.instance["port_name"] = name
        return True


class NameDlg(wx.Dialog):

    """Name Editing Dialog.
    
    - Contains a scrolled area with a text box for each parameter.
    - Contains a non-scrolled area with standard dialog buttons.

    """

    def __init__(self, instance, names, *args, **kwargs):
        wx.Dialog.__init__(self, *args, **kwargs)
        self.SetExtraStyle(wx.WS_EX_VALIDATE_RECURSIVELY)
        panel = wx.Panel(self, -1)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        sb = wx.StaticBox(panel, -1, "Name:")
        hsizer = wx.StaticBoxSizer(sb, wx.HORIZONTAL)
        hsizer.Add(wx.TextCtrl(
            panel, 
            validator=PythonExpValidator(instance, names)
        ), 1, wx.ALIGN_CENTER)
        vsizer.Add(hsizer, 0, wx.EXPAND)
        panel.SetSizer(vsizer)
        wvsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(wx.Button(self, wx.ID_OK, "OK"), 0, wx.ALIGN_BOTTOM)
        hsizer.Add(wx.Button(self, wx.ID_CANCEL, "Cancel"), 0, wx.ALIGN_BOTTOM)
        wvsizer.Add(panel, 1, wx.EXPAND)
        wvsizer.Add(hsizer, 0, wx.ALIGN_RIGHT)
        self.SetSizer(wvsizer)
