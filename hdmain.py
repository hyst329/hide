from hdver import verstr
from hdeditor import HideEditor

__author__ = 'hyst329'
import wx
import wx.lib.dialogs
import wx.stc
import json
import subprocess


class MainIDEFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainIDEFrame, self).__init__(parent, title=title, size=(800, 600))

        # Loading the config
        self.config = json.load(open("config.json", "r"))
        self.helpath = self.config["helpath"]

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        editMenu = wx.Menu()
        projectMenu = wx.Menu()
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
        newProjectMenuItem = projectMenu.Append(wx.ID_ANY, "New Project", "Create new project")
        openProjectMenuItem = projectMenu.Append(wx.ID_ANY, "Open Project...", "Create new project")
        saveProjectMenuItem = projectMenu.Append(wx.ID_ANY, "Save Project", "Create new project")
        saveProjectAsMenuItem = projectMenu.Append(wx.ID_ANY, "Save Project As...", "Create new project")
        closeProjectMenuItem = projectMenu.Append(wx.ID_ANY, "Close Project", "Create new project")
        runMenuItem = runMenu.Append(wx.ID_ANY, "Run\tF9", "Runs the project")
        generateMenuItem = runMenu.Append(wx.ID_ANY, "Generate C file\tF10", "Generate C code from project")
        genAndCompMenuItem = runMenu.Append(wx.ID_ANY, "Generate and compile\tF11",
                                            "Generate and try to compile it with GCC")
        aboutMenuItem = helpMenu.Append(wx.ID_ANY, "About\tCtrl+F1", "Display info about hide")
        menubar.Append(fileMenu, "&File")
        menubar.Append(editMenu, "&Edit")
        menubar.Append(projectMenu, "&Project")
        menubar.Append(runMenu, "&Run")
        menubar.Append(helpMenu, "&Help")
        for mi in projectMenu.GetMenuItems():
            mi.Enable(False)
        self.SetMenuBar(menubar)
        font = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_NORMAL, False, 'Fixedsys',
                       wx.FONTENCODING_CP1252)
        self.editor = HideEditor(self, font=font)
        self.output = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.output.SetFont(font)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.editor, 5, wx.EXPAND)
        self.sizer.Add(self.output, 3, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.sb = self.CreateStatusBar()

        self.Bind(wx.EVT_MENU, self.OnNew, newMenuItem)
        self.Bind(wx.EVT_MENU, self.OnOpen, openMenuItem)
        self.Bind(wx.EVT_MENU, self.OnSave, saveMenuItem)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, saveAsMenuItem)
        self.Bind(wx.EVT_MENU, self.OnQuit, quitMenuItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutMenuItem)
        self.Bind(wx.EVT_MENU, self.OnRun, runMenuItem)
        self.Bind(wx.EVT_MENU, self.OnGenerate, generateMenuItem)
        self.Bind(wx.EVT_MENU, self.OnGenAndComp, genAndCompMenuItem)

        self.timer = wx.Timer(self, wx.ID_ANY)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

        self.timer.Start(1000)

        self.Layout()
        self.Centre()
        self.Show()

    def OnNew(self, e):
        pass

    def OnOpen(self, e):
        dlg = wx.FileDialog(self, message="Open", wildcard="F4/Helen sources (*.f4)|*.f4",
                            style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_CANCEL:
            return
        fname = dlg.GetPath()
        self.editor.filename = fname
        f = open(fname, 'r')
        self.editor.SetText(f.read())
        f.close()
        dlg.Destroy()
        self.editor.modified = False
        pass

    def OnSave(self, e):
        if not self.editor.filename:
            self.OnSaveAs(e)
        else:
            f = open(self.editor.filename, 'w')
            f.write(self.editor.GetText())
            f.close()
            self.editor.modified = False

    def OnSaveAs(self, e):
        dlg = wx.FileDialog(self, message="Save As", wildcard="F4/Helen sources (*.f4)|*.f4",
                            style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_CANCEL:
            return
        fname = dlg.GetPath()
        f = open(fname, 'w')
        f.write(self.editor.GetText())
        f.close()
        self.editor.modified = False
        dlg.Destroy()

    def OnQuit(self, e):
        self.Close()

    def OnAbout(self, e):
        about = "hide - Helen IDE\nVersion %s" \
                "\nCopyright 2015 by hyst329" \
                "\nPowered by wxPython toolkit" % verstr
        dlg = wx.lib.dialogs.ScrolledMessageDialog(self, about, "About hide")
        dlg.ShowModal()
        dlg.Destroy()

    def OnTimer(self, e):
        s = "hide - %s%s" % (self.editor.filename, "*" if self.editor.modified else "")
        self.SetTitle(s)

    def OnRun(self, e):
        if not self.editor.filename:
            wx.MessageBox("Please save the file first!", "File needs to be saved")
            return
        elif self.editor.modified:
            self.OnSave(e)
        cmd = "%s %s -i" % (self.helpath, self.editor.filename)
        out = subprocess.check_output(cmd)
        self.output.Clear()
        self.output.SetValue(out)

    def OnGenerate(self, e):
        if not self.editor.filename:
            wx.MessageBox("Please save the file first!", "File needs to be saved")
            return
        elif self.editor.modified:
            self.OnSave(e)
        cmd = "%s %s -g" % (self.helpath, self.editor.filename)
        out = subprocess.check_output(cmd)
        self.output.Clear()
        self.output.SetValue(out)

    def OnGenAndComp(self, e):
        if not self.editor.filename:
            wx.MessageBox("Please save the file first!", "File needs to be saved")
            return
        elif self.editor.modified:
            self.OnSave(e)
        cmd = "%s %s -gc" % (self.helpath, self.editor.filename)
        out = subprocess.check_output(cmd)
        self.output.Clear()
        self.output.SetValue(out)


if __name__ == '__main__':
    app = wx.App()
    MainIDEFrame(None, title='hide')
    app.MainLoop()

