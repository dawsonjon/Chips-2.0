#!/usr/bin/env python

import sys
import os
import webbrowser
import subprocess

import wx
from wx.lib.wordwrap import wordwrap

import docwin

license_text = """
Copyright (c) 2012 Jonathan P Dawson

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.  

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

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
        self.file_export_html  = file_menu.Append(-1, "Export HTML")
        self.file_export_latex  = file_menu.Append(-1, "Export Latex")
        self.file_export_odt  = file_menu.Append(-1, "Export odt")
        self.file_exit    = file_menu.Append(wx.ID_EXIT, "Exit")

        self.Bind(wx.EVT_MENU, self.on_open,    self.file_open)
        self.Bind(wx.EVT_MENU, self.on_save,    self.file_save)
        self.Bind(wx.EVT_MENU, self.on_save_as, self.file_save_as)
        self.Bind(wx.EVT_MENU, self.on_export_html,  self.file_export_html)
        self.Bind(wx.EVT_MENU, self.on_export_latex,  self.file_export_latex)
        self.Bind(wx.EVT_MENU, self.on_export_odt,  self.file_export_odt)
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
        self.insert_italics = insert_menu.Append(-1, "Italics")
        self.insert_bold = insert_menu.Append(-1, "Bold")
        self.insert_csv_2_table = insert_menu.Append(-1, "CSV 2 Table")
        self.insert_table_2_csv = insert_menu.Append(-1, "Table 2 CSV")
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
        self.Bind(wx.EVT_MENU, self.on_insert_italics, self.insert_italics)
        self.Bind(wx.EVT_MENU, self.on_insert_bold, self.insert_bold)
        self.Bind(wx.EVT_MENU, self.on_insert_table_2_csv, self.insert_table_2_csv)
        self.Bind(wx.EVT_MENU, self.on_insert_csv_2_table, self.insert_csv_2_table)
        self.Bind(wx.EVT_MENU, self.on_insert_image, self.insert_image)
        self.Bind(wx.EVT_MENU, self.on_insert_link, self.insert_link)
        self.Bind(wx.EVT_MENU, self.on_insert_sample, self.insert_sample)

        help_menu = wx.Menu()
        self.help_quick = help_menu.Append(-1, "reST Quick Start Guide")
        self.help_spec =  help_menu.Append(-1, "reST Specification")
        self.help_about = help_menu.Append(-1, "About")

        self.Bind(wx.EVT_MENU, self.on_help_quick, self.help_quick)
        self.Bind(wx.EVT_MENU, self.on_help_spec, self.help_spec)
        self.Bind(wx.EVT_MENU, self.on_help_about, self.help_about)


        menubar.Append(file_menu, "File")
        menubar.Append(edit_menu, "Edit")
        menubar.Append(insert_menu, "Insert")
        menubar.Append(help_menu, "Help")
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
        self.Bind(wx.EVT_CLOSE, self.on_exit)
        self.Bind(wx.EVT_FIND, self.on_find)
        self.Bind(wx.EVT_FIND_NEXT, self.on_find)
        self.Bind(wx.EVT_FIND_REPLACE, self.on_find_replace)
        self.Bind(wx.EVT_FIND_REPLACE_ALL, self.on_find_replace_all)

        sizer=wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        panel.Layout()
        self.Layout()

        self.editor = editor
        self.viewer = viewer

        #application state
        self.saved = False
        self.undos = [""]
        self.redos = []

    def open(self, rst_file):
        input_file = rst_file
        self.editor.SetValue(input_file.read())
        input_file.close()
        self.saved = True
        self.undos = [""]
        self.redos = []

    def on_open(self, event):
        dlg = wx.FileDialog(
                self, message="Open reST File",
                defaultDir=os.getcwd(), 
                defaultFile="",
                wildcard="reStructuredText file (*.rst)|*.rst|"\
                         "Text file (*.txt)|*.txt|"\
                         "All files (*.*)|*.*",
                style=wx.OPEN) 

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.filename = path
            input_file = open(path)
            self.editor.SetValue(input_file.read())
            input_file.close()
            self.saved = True
            self.SetTitle("reSTEd - (%s)"%self.filename)
            self.undos = [""]
            self.redos = []

    def on_save(self, event):
        if not hasattr(self, "filename"):
            dlg = wx.FileDialog(
                    self, message="Save reST File",
                    defaultDir=os.getcwd(), 
                    defaultFile="",
                    wildcard="reStructuredText file (*.rst)|*.rst|"\
                             "Text file (*.txt)|*.txt|"\
                             "All files (*.*)|*.*",
                    style=wx.SAVE) 

            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                self.filename = path

        if hasattr(self, "filename"):
            output_file = open(self.filename, "w")
            output_file.write(self.editor.GetValue())
            output_file.close()
            self.saved = True
            self.SetTitle("reSTEd - (%s)"%self.filename)

    def on_save_as(self, event):
        dlg = wx.FileDialog(
                self, message="Save reST File",
                defaultDir=os.getcwd(), 
                defaultFile="",
                wildcard="reStructuredText file (*.rst)|*.rst|"\
                         "Text file (*.txt)|*.txt|"\
                         "All files (*.*)|*.*",
                style=wx.SAVE) 

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.filename = path
            output_file = open(self.filename, "w")
            output_file.write(self.editor.GetValue())
            output_file.close()
            self.saved = True
            self.SetTitle("reSTEd - (%s)"%self.filename)

    def on_help_quick(self, event):
        webbrowser.open("http://docutils.sourceforge.net/docs/user/rst/quickref.html")

    def on_help_spec(self, event):
        webbrowser.open("http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html")

    def on_help_about(self, event):
        info = wx.AboutDialogInfo()
        info.Name = "reSTEd"
        info.Version = "0.0.1"
        info.Copyright = "Copyright (C) 2012 Jonathan P Dawson"
        info.Description = "An editor for reStructuredText"
        info.WebSite = ("http://github.com/dawsonjon/reSTEd", "Fork reSTEd on github")
        info.Developers = [ "Jon Dawson"]
        info.License = wordwrap(license_text, 500, wx.ClientDC(self))
        wx.AboutBox(info)

    def on_export_html(self, event):
        dlg = wx.FileDialog(
                self, message="Export HTML File",
                defaultDir=os.getcwd(), 
                defaultFile="",
                wildcard="HTML files (*.htm, *.html)|*htm;*.html|"\
                         "All files (*.*)|*.*",
                style=wx.SAVE) 

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.viewer.export_html(path)
            webbrowser.open(path)

    def on_export_latex(self, event):
        dlg = wx.FileDialog(
                self, message="Export Latex File",
                defaultDir=os.getcwd(), 
                defaultFile="",
                wildcard="Latex files (*.tex)|*.tex|"\
                         "All files (*.*)|*.*",
                style=wx.SAVE) 

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.viewer.export_latex(path)

    def on_export_odt(self, event):
        dlg = wx.FileDialog(
                self, message="Export ODT File",
                defaultDir=os.getcwd(), 
                defaultFile="",
                wildcard="odt files (*.odt)|*.odt|"\
                         "All files (*.*)|*.*",
                style=wx.SAVE) 

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            path = dlg.GetPath()
            self.viewer.export_odt(path)

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
        if not self.saved:
            dlg = wx.MessageDialog(
                    self, 
                    "Do you want to save changes?",
                    "Save Changes?",
                    wx.YES_NO | wx.CANCEL)
            result = dlg.ShowModal()
            if result == wx.ID_CANCEL:
                return
            if result == wx.ID_YES:
                self.on_save(None)
        self.Destroy()

    def on_text(self, event):
        self.saved=False
        if hasattr(self, "filename"):
            self.SetTitle("*reSTEd - (%s)"%self.filename)
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
            self.editor.Replace(f, t, "\n\n.. image:: %s\n\n"%path)

    def on_insert_link(self, event):

        f, t = self.editor.GetSelection()
        selection = self.editor.GetString(f, t)
        if not selection:
            selection = "hyperlink text"
        self.editor.Replace(f, t, "`%s <http://your_url_here>`_ "%selection)

    def on_insert_title(self, event):

        f, t = self.editor.GetSelection()
        selection = self.editor.GetString(f, t)
        if not selection:
            selection = "title"
        line = "".join(["=" for i in selection])    
        self.editor.Replace(f, t, "\n\n%s\n%s\n%s\n"%(line, selection, line))

    def on_insert_subtitle(self, event):

        f, t = self.editor.GetSelection()
        selection = self.editor.GetString(f, t)
        if not selection:
            selection = "subtitle"
        line = "".join(["-" for i in selection])    
        self.editor.Replace(f, t, "\n\n%s\n%s\n%s\n"%(line, selection, line))

    def on_insert_chapter(self, event):

        f, t = self.editor.GetSelection()
        selection = self.editor.GetString(f, t)
        if not selection:
            selection = "chapter"
        line = "".join(["=" for i in selection])    
        self.editor.Replace(f, t, "\n\n%s\n%s\n"%(selection, line))

    def on_insert_section(self, event):

        f, t = self.editor.GetSelection()
        selection = self.editor.GetString(f, t)
        if not selection:
            selection = "section"
        line = "".join(["-" for i in selection])    
        self.editor.Replace(f, t, "\n\n%s\n%s\n"%(selection, line))

    def on_insert_subsection(self, event):

        f, t = self.editor.GetSelection()
        selection = self.editor.GetString(f, t)
        if not selection:
            selection = "subsection"
        line = "".join(["^" for i in selection])    
        self.editor.Replace(f, t, "\n\n%s\n%s\n"%(selection, line))

    def on_insert_italics(self, event):

        f, t = self.editor.GetSelection()
        selection = self.editor.GetString(f, t)
        if not selection:
            selection = "italics"
        selection = selection.strip()
        self.editor.Replace(f, t, " *%s* "%selection)

    def on_insert_bold(self, event):

        f, t = self.editor.GetSelection()
        selection = self.editor.GetString(f, t)
        if not selection:
            selection = "bold"
        selection = selection.strip()
        self.editor.Replace(f, t, " **%s** "%selection)

    def on_insert_bullets(self, event):

        f, t = self.editor.GetSelection()
        selection = self.editor.GetString(f, t)
        if not selection:
            selection = "\nitem\nitem\n\n"

        selection = selection.strip()
        selection = "\n".join(["+ "+i for i in selection.splitlines()])
        self.editor.Replace(f, t, "\n\n" + selection + "\n\n")

    def on_insert_numbering(self, event):

        f, t = self.editor.GetSelection()
        selection = self.editor.GetString(f, t)
        if not selection:
            selection = "\nitem\nitem\n\n"

        selection = selection.strip()
        selection = "\n".join(["#. "+i for i in selection.splitlines()])
        self.editor.Replace(f, t, "\n\n" + selection + "\n\n")

    def on_insert_csv_2_table(self, event):
        f, t = self.editor.GetSelection()
        selection = self.editor.GetString(f, t)
        if not selection:
            selection = "1, 2, 3\n4, 5, 6\n"

        self.editor.Replace(f, t, "\n" + self.csv_2_table(selection) + "\n")

    def on_insert_table_2_csv(self, event):
        f, t = self.editor.GetSelection()
        selection = self.editor.GetString(f, t)
        self.editor.Replace(f, t, "\n" + self.table_2_csv(selection) + "\n")

    def on_insert_sample(self, event):
        f, t = self.editor.GetSelection()
        selection = self.editor.GetString(f, t)
        if not selection:
            selection = "code sample"
        selection = self.indent(selection)
        self.editor.Replace(f, t, "\n::\n\n%s\n"%selection)

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

    def csv_2_table(self, csv):

        widths = self.get_column_widths(csv)
        widths = [widths[i] for i in range(len(widths))]
        seperator = ["".join(["-" for i in range(w+2)]) for w in widths]
        seperator = "+" + "+".join(seperator) + "+"

        table = []
        for line in csv.splitlines():
            table.append(seperator)
            cols = "|".join([i.strip().center(w+2) for i, w in zip(line.split(","), widths)])
            cols = "|" + cols + "|" 
            table.append(cols)
        table.append(seperator)
        return "\n".join(table)

    def get_column_widths(self, csv):
        widths = {}
        for line in csv.splitlines():
            for number, column in enumerate(line.split(",")):
                width = len(column.strip())
                if number not in widths:
                    widths[number] = width
                else:
                    if width > widths[number]:
                        widths[number] = width
        return widths

    def table_2_csv(self, table):
        csv = []
        for line in table.splitlines():
            line = line.strip("|")
            if "|" in line:
                cols = line.split("|")
                csv.append(", ".join([i.strip() for i in cols]))
        return "\n".join(csv)

    def indent(self, text):
        return "\n".join(["    " + i for i in text.splitlines()])

if __name__ == "__main__":
    app = wx.App()
    frame = DocEdit(None, title="reSTEd", size=(1024,768))
    frame.Show()
    if len(sys.argv) > 1:
        rst_file = open(sys.argv[1])
        frame.open(rst_file)

    app.MainLoop()
