import wx

class BreakPointDialog(wx.Dialog):
    def __init__(self, parent, files):
        wx.Dialog.__init__(self, parent, -1, "Set Breakpoint")

        sizer = wx.BoxSizer(wx.VERTICAL)
        files_list = wx.ListCtrl(self, -1)
        print files
        for f in files:
            files_list.Append(f,f)

        sizer.Add(files_list, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

