from hdver import verstr

__author__ = 'hyst329'
import wx
import wx.lib.dialogs
import wx.stc


class MainIDEFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainIDEFrame, self).__init__(parent, title=title, size=(800, 600))

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        editMenu = wx.Menu()
        runMenu = wx.Menu()
        helpMenu = wx.Menu()
        newMenuItem = fileMenu.Append(wx.ID_ANY, "New\tCtrl+N", "Create a new .f4 file")
        openMenuItem = fileMenu.Append(wx.ID_ANY, "Open...\tCtrl+O", "Open existing .f4 file")
        saveMenuItem = fileMenu.Append(wx.ID_ANY, "Save\tCtrl+S", "Save the file")
        saveAsMenuItem = fileMenu.Append(wx.ID_ANY, "Save As...\tCtrl+Shift+S", "Save the file")
        quitMenuItem = fileMenu.Append(wx.ID_ANY, "Quit\tAlt+F4", "Quit application")
        cutMenuItem = editMenu.Append(wx.ID_ANY, "Cut\tCtrl+X", "Move the selection to clipboard")
        copyMenuItem = editMenu.Append(wx.ID_ANY, "Copy\tCtrl+C", "Copy the selection to clipboard")
        pasteMenuItem = editMenu.Append(wx.ID_ANY, "Paste\tCtrl+V", "Copy clipboard contents to the selection")
        runMenuItem = runMenu.Append(wx.ID_ANY, "Run\tF9", "Runs the project")
        runMenuItem = runMenu.Append(wx.ID_ANY, "Generate C file\tF10", "Generate C code from project")
        runMenuItem = runMenu.Append(wx.ID_ANY, "Generate and compile\tF11", "Generate and try to compile it with GCC")
        aboutMenuItem = helpMenu.Append(wx.ID_ANY, "About\tCtrl+F1", "Display info about hide")
        menubar.Append(fileMenu, "&File")
        menubar.Append(editMenu, "&Edit")
        menubar.Append(runMenu, "&Run")
        menubar.Append(helpMenu, "&Help")
        self.SetMenuBar(menubar)

        self.sizer = wx.GridSizer(2, 2, 5, 5)
        self.editor = wx.stc.StyledTextCtrl()
        self.sizer.Add(self.editor, 1, wx.ALIGN_RIGHT)
        self.SetSizer(self.sizer)

        self.Bind(wx.EVT_MENU, self.OnNew, newMenuItem)
        self.Bind(wx.EVT_MENU, self.OnQuit, quitMenuItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutMenuItem)

        self.Centre()
        self.Show()

    def OnNew(self, e):
        pass

    def OnQuit(self, e):
        self.Close()

    def OnAbout(self, e):
        about = "hide - Helen IDE\nVersion %s" \
                "\nCopyright 2015 by hyst329" \
                "\nPowered by wxPython toolkit" % verstr
        dlg = wx.lib.dialogs.ScrolledMessageDialog(self, about, "About hide")
        dlg.ShowModal()
        dlg.Destroy()

if __name__ == '__main__':
    app = wx.App()
    MainIDEFrame(None, title='hide')
    app.MainLoop()

