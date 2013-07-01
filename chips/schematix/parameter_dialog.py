import wx
from wx.lib.scrolledpanel import ScrolledPanel

class PythonExpValidator(wx.PyValidator):

    """A python expression validator.
    
    * Tranfers Data to and from windows in a dialog box.
    * Checks that entered data is a valid python expression
    """

    def __init__(self, parameters, parameter):
        wx.PyValidator.__init__(self)
        self.parameter = parameter
        self.parameters = parameters

    def Clone(self):
        return PythonExpValidator(self.parameters, self.parameter)

    def Validate(self, win):
        textctrl = self.GetWindow()
        text = textctrl.GetValue()
        try:
            eval(text)
            textctrl.SetBackgroundColour(
                wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
            )
            textctrl.Refresh()
        except Exception as inst:
            valid = False
            wx.MessageBox(
            """Parameter must be a valid python expression
            {0} 
            raised the following exception:
            {1}""".format(text, inst))
            textctrl.SetBackgroundColour("pink")
            textctrl.SetFocus()
            textctrl.Refresh()
            return False
        return True

    def TransferToWindow(self):
        self.GetWindow().SetValue(
            self.parameters[self.parameter]
        )
        return True

    def TransferFromWindow(self):
        text = self.GetWindow().GetValue()
        self.parameters[self.parameter] = text
        return True


class ParameterDlg(wx.Dialog):

    """Parameter Editing Dialog.
    
    - Contains a scrolled area with a text box for each parameter.
    - Contains a non-scrolled area with standard dialog buttons.

    """

    def __init__(self, parameters, *args, **kwargs):
        wx.Dialog.__init__(self, title="Edit Parameters", *args, **kwargs)
        self.SetExtraStyle(wx.WS_EX_VALIDATE_RECURSIVELY)
        panel = ScrolledPanel(self, -1)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        for parameter in parameters:
            sb = wx.StaticBox(panel, -1, str(parameter))
            hsizer = wx.StaticBoxSizer(sb, wx.HORIZONTAL)
            hsizer.Add(wx.TextCtrl(
                panel, 
                validator=PythonExpValidator(parameters, parameter)
            ), 1, wx.ALIGN_CENTER)
            vsizer.Add(hsizer, 0, wx.EXPAND)
        panel.SetSizer(vsizer)
        panel.SetupScrolling()
        wvsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(wx.Button(self, wx.ID_OK, "OK"), 0, wx.ALIGN_BOTTOM)
        hsizer.Add(wx.Button(self, wx.ID_CANCEL, "Cancel"), 0, wx.ALIGN_BOTTOM)
        wvsizer.Add(panel, 1, wx.EXPAND)
        wvsizer.Add(hsizer, 0, wx.ALIGN_RIGHT)
        self.SetSizer(wvsizer)
