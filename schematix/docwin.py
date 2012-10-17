#!/usr/bin/env python
import wx
import wx.html as html
import docutils.core

class DocWin(html.HtmlWindow):

    """RsT Help viewer window"""

    def __init__(self, *args):
        html.HtmlWindow.__init__(self, *args)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

    def set_RsT(self, RsT):
        document = docutils.core.publish_doctree(RsT)
        html = docutils.core.publish_from_doctree(document, writer_name="html")
        self.SetPage(html)


if __name__ == "__main__":

    test_document = """

section
=======

subsection
----------

Some text in a paragraph.

Some text in a paragraph.

subsection
----------

A bulleted list of random characters:

+ asdfasdf
+ asdfasdfasdfasdf
+ asds

A numbered list:

1. blah
2. blah blah
3. blah blah

subsection
----------

Table:

+---------+---------------+
| Header  | Other Header  |
+=========+===============+
| row1    |  column 2     |
+---------+---------------+
| row2    |  column 2     |
+---------+---------------+

Preformatted Text::
    def myfunction():
        pass

You can also add links_ to addresses.

.. _links: http://www.google.com

"""

    app = wx.App()
    frame = wx.Frame(None, size=(800,600), title="Test Help Window")
    docwin = DocWin(frame, -1)
    docwin.set_RsT(test_document)
    frame.Show()
    #frame.SetSizer(docwin)
    app.MainLoop()
