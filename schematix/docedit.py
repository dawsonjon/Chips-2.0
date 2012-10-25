import os

import wx

import docwin

class DocEdit(wx.Frame):

    def __init__(self, *args, **vargs):
        wx.Frame.__init__(self, *args, **vargs)
        panel = wx.Panel(self, -1)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)

        #make menu
        menubar = wx.MenuBar()

        file_menu = wx.Menu()

        self.file_open    = file_menu.Append(wx.ID_OPEN, "Open")
        self.file_save    = file_menu.Append(wx.ID_SAVE, "Save")
        self.file_save_as = file_menu.Append(wx.ID_SAVEAS, "Save As")
        self.file_export  = file_menu.Append(-1, "Export")
        self.file_exit    = file_menu.Append(wx.ID_EXIT, "Exit")

        self.Bind(wx.EVT_MENU, self.on_open,    self.file_open)
        self.Bind(wx.EVT_MENU, self.on_save,    self.file_save)
        self.Bind(wx.EVT_MENU, self.on_save_as, self.file_save_as)
        self.Bind(wx.EVT_MENU, self.on_export,  self.file_export)
        self.Bind(wx.EVT_MENU, self.on_exit,    self.file_exit)


        edit_menu = wx.Menu()
        self.edit_undo = edit_menu.Append(wx.ID_UNDO, "Undo")
        self.edit_redo = edit_menu.Append(wx.ID_REDO, "Redo")
        self.edit_find = edit_menu.Append(-1, "Find")
        self.edit_replace = edit_menu.Append(-1, "Replace")

        self.Bind(wx.EVT_MENU, self.on_undo, self.edit_undo)
        self.Bind(wx.EVT_MENU, self.on_redo, self.edit_redo)
        self.Bind(wx.EVT_MENU, self.on_show_find, self.edit_find)
        self.Bind(wx.EVT_MENU, self.on_show_replace, self.edit_replace)

        self.edit_undo.Enable(False)
        self.edit_redo.Enable(False)

        insert_menu = wx.Menu()

        self.insert_title = insert_menu.Append(-1, "Title")
        self.insert_subtitle = insert_menu.Append(-1, "Subtitle")
        self.insert_chapter = insert_menu.Append(-1, "Chapter")
        self.insert_section = insert_menu.Append(-1, "Section")
        self.insert_subsection = insert_menu.Append(-1, "Subsection")
        self.insert_bullets = insert_menu.Append(-1, "Bullets")
        self.insert_numbering = insert_menu.Append(-1, "Numbering")
        self.insert_table = insert_menu.Append(-1, "Table")
        self.insert_image = insert_menu.Append(-1, "Image")
        self.insert_link = insert_menu.Append(-1, "Hyperlink")
        self.insert_sample = insert_menu.Append(-1, "Code Sample")

        self.Bind(wx.EVT_MENU, self.on_insert_title, self.insert_title)
        self.Bind(wx.EVT_MENU, self.on_insert_subtitle, self.insert_subtitle)
        self.Bind(wx.EVT_MENU, self.on_insert_chapter, self.insert_chapter)
        self.Bind(wx.EVT_MENU, self.on_insert_section, self.insert_section)
        self.Bind(wx.EVT_MENU, self.on_insert_subsection, self.insert_subsection)
        self.Bind(wx.EVT_MENU, self.on_insert_bullets, self.insert_bullets)
        self.Bind(wx.EVT_MENU, self.on_insert_numbering, self.insert_numbering)
        self.Bind(wx.EVT_MENU, self.on_insert_table, self.insert_table)
        self.Bind(wx.EVT_MENU, self.on_insert_image, self.insert_image)
        self.Bind(wx.EVT_MENU, self.on_insert_link, self.insert_link)
        self.Bind(wx.EVT_MENU, self.on_insert_sample, self.insert_sample)


        menubar.Append(file_menu, "File")
        menubar.Append(edit_menu, "Edit")
        menubar.Append(insert_menu, "Insert")
        self.SetMenuBar(menubar)

        editor = wx.TextCtrl(panel,  -1, style=wx.TE_MULTILINE|wx.TE_RICH)
        font1 = wx.Font(12, wx.TELETYPE, wx.NORMAL, wx.NORMAL, False)
        editor.SetFont(font1)
        viewer = docwin.DocWin(panel, -1)

        vsizer.Add(hsizer, 1, wx.EXPAND)
        hsizer.Add(editor, 1, wx.EXPAND)
        hsizer.Add(viewer, 1, wx.EXPAND)

        panel.SetSizer(vsizer)
        self.Bind(wx.EVT_TEXT, self.on_text)
        self.Bind(wx.EVT_FIND, self.on_find)
        self.Bind(wx.EVT_FIND_NEXT, self.on_find)
        self.Bind(wx.EVT_FIND_REPLACE, self.on_find_replace)
        self.Bind(wx.EVT_FIND_REPLACE_ALL, self.on_find_replace_all)

        self.editor = editor
        self.viewer = viewer

        #application state
        self.saved = False
        self.undos = [""]
        self.redos = []

    def on_open(self, event):
        dlg = wx.FileDialog(
                self, message="Open reST File",
                defaultDir=os.getcwd(), 
                defaultFile="",
                style=wx.OPEN) 

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.filename = path
            input_file = open(path)
            self.editor.SetValue(input_file.read())
            input_file.close()
            self.saved = True
            self.undos = [""]
            self.redos = []

    def on_save(self, event):
        if not hasattr(self, "filename"):
            dlg = wx.FileDialog(
                    self, message="Save reST File",
                    defaultDir=os.getcwd(), 
                    defaultFile="",
                    style=wx.SAVE) 

            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                self.filename = path

        if hasattr(self, "filename"):
            output_file = open(self.filename, "w")
            output_file.write(self.editor.GetValue())
            output_file.close()
            self.saved = True

    def on_save_as(self, event):
        dlg = wx.FileDialog(
                self, message="Save reST File",
                defaultDir=os.getcwd(), 
                defaultFile="",
                style=wx.SAVE) 

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.filename = path
            output_file = open(self.filename, "w")
            output_file.write(self.editor.GetValue())
            output_file.close()
            self.saved = True

    def on_export(self, event):
        pass

    def on_undo(self, event):
        if len(self.undos) > 1:
            text = self.undos.pop()
            self.redos.append(text)
            self.editor.SetValue(self.undos[-1])
            self.undos.pop()#setvalue causes text event which adds another undo
            self.edit_redo.Enable(True)
        if len(self.undos) <= 1:
            self.edit_undo.Enable(False)

    def on_redo(self, event):
        if self.redos:
            text = self.redos.pop()
            self.undos.append(text)
            self.editor.SetValue(text)
            self.undos.pop()#setvalue causes text event which adds another undo
            self.edit_undo.Enable(True)
        if not self.redos:
            self.edit_redo.Enable(False)

    def on_exit(self, event):
        self.Destroy()

    def on_text(self, event):
        self.saved=False
        self.edit_undo.Enable(True)

        text = self.editor.GetValue()
        self.undos.append(text)
        self.viewer.set_RsT(text)

    def on_insert_image(self, event):

        dlg = wx.FileDialog(
                self, message="Insert Image",
                defaultDir=os.getcwd(), 
                defaultFile="",
                style=wx.OPEN) 

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            f, t = self.editor.GetSelection()
            self.editor.Replace(f, t, "\n.. image:: %s\n"%path)

    def on_insert_link(self, event):

        f, t = self.editor.GetSelection()
        selection = self.editor.GetString(f, t)
        self.editor.Replace(f, t, "`%s <http://your_url_here>`_ "%selection)

    def on_insert_title(self, event):

        f, t = self.editor.GetSelection()
        selection = self.editor.GetString(f, t)
        self.editor.Replace(f, t, "\n========\n%s\n========\n"%selection)

    def on_insert_subtitle(self, event):

        f, t = self.editor.GetSelection()
        selection = self.editor.GetString(f, t)
        self.editor.Replace(f, t, "\n----------\n%s\n----------\n"%selection)

    def on_insert_chapter(self, event):

        f, t = self.editor.GetSelection()
        selection = self.editor.GetString(f, t)
        self.editor.Replace(f, t, "\n%s\n========\n"%selection)

    def on_insert_section(self, event):

        f, t = self.editor.GetSelection()
        selection = self.editor.GetString(f, t)
        self.editor.Replace(f, t, "\n%s\n--------\n"%selection)

    def on_insert_subsection(self, event):

        f, t = self.editor.GetSelection()
        selection = self.editor.GetString(f, t)
        self.editor.Replace(f, t, "\n%s\n^^^^^^^^^^^\n"%selection)

    def on_insert_bullets(self, event):

        f, t = self.editor.GetSelection()
        selection = self.editor.GetString(f, t)
        self.editor.Replace(f, t, "\n+ item\n+ item\n\n  + subitem\n\n"%selection)

    def on_insert_numbering(self, event):

        f, t = self.editor.GetSelection()
        selection = self.editor.GetString(f, t)
        self.editor.Replace(f, t, "\n1. item\n2. item\n\n  1. subitem\n\n"%selection)

    def on_show_find(self, event):
        data = wx.FindReplaceData()
        self.find_dlg = wx.FindReplaceDialog(self, data, "Find")
        self.find_dlg.data = data
        self.find_dlg.Show(True)

    def on_show_replace(self, event):
        data = wx.FindReplaceData()
        self.find_dlg = wx.FindReplaceDialog(self, data, "Find & Replace", wx.FR_REPLACEDIALOG)
        self.find_dlg.data = data
        self.find_dlg.Show(True)

    def on_find(self, event):
        start = self.editor.GetInsertionPoint()
        t, f = self.editor.GetSelection()
        find = event.GetFindString()
        text = self.editor.GetValue()
        down = event.GetFlags() & 1
        if down:
            text = text[f:]
            position = text.find(find)
            if position < 0:
                wx.MessageBox("end of document")
                self.editor.SetInsertionPointEnd()
            else:
                self.editor.SetSelection(position + f, position + f + len(find))
        else:
            text = text[:t]
            position = text.rfind(find)
            if position < 0:
                wx.MessageBox("start of document")
                self.editor.SetInsertionPoint(0)
            else:
                self.editor.SetSelection(position, position + len(find))

    def on_find_replace(self, event):
        start = self.editor.GetInsertionPoint()
        t, f = self.editor.GetSelection()
        find = event.GetFindString()
        replace = event.GetReplaceString()
        text = self.editor.GetValue()
        down = event.GetFlags() & 1
        if down:
            text = text[t:]
            position = text.find(find)
            if position < 0:
                wx.MessageBox("end of document")
                self.editor.SetInsertionPointEnd()
            else:
                self.editor.Replace(position + t, position + t + len(find), replace)
        else:
            text = text[:f]
            position = text.rfind(find)
            if position < 0:
                wx.MessageBox("start of document")
                self.editor.SetInsertionPoint(0)
            else:
                self.editor.Replace(position, position + len(find), replace)

    def on_find_replace_all(self, event):
        find = event.GetFindString()
        replace = event.GetReplaceString()
        text = self.editor.GetValue()
        text.replace(find, replace)
        self.editor.SetValue(text)

    def on_insert_table(self, event):

        f, t = self.editor.GetSelection()

        rows = self.rows.GetValue()
        cols = self.cols.GetValue()

        hline = "----------".join(["+" for i in range(cols+1)])
        vline = "          ".join(["|" for i in range(cols+1)])
        table = (vline + "\n").join([hline + "\n" for i in range(rows + 1)])

        self.editor.Replace("\n" + table + "\n")

    def on_insert_sample(self, event):
        pass


if __name__ == "__main__":
    app = wx.App()
    frame = DocEdit(None, title="reST Editor", size=(1024,768))
    frame.Show()
    app.MainLoop()
