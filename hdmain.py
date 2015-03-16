import sys
from hdsettings import SettingsDialog
from hdver import verstr, verstrs
from hdeditor import HideEditor

__author__ = 'hyst329'
import wx
import wx.lib.dialogs
import wx.stc
import wx.adv
import json
import subprocess
import os


class MainIDEFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainIDEFrame, self).__init__(parent, title=title, size=(800, 600))

        # Loading the config
        if getattr(sys, 'frozen', False):
            path = os.path.dirname(sys.executable)
        else:
            path = os.path.dirname(os.path.realpath(__file__))
        if os.path.isfile(path + "/config.json"):
            cfg = open("config.json", "r")
            self.config = json.load(cfg)
        else:
            wx.MessageBox("No config file found. Creating new - please check your settings",
                          "Warning", wx.ICON_WARNING)
            self.config = {"helpath": "C:/f4main/f4main.exe"}
            cfg = open("config.json", "w")
            json.dump(self.config, cfg)
        self.helpath = self.config["helpath"]

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        editMenu = wx.Menu()
        projectMenu = wx.Menu()
        optionsMenu = wx.Menu()
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
        openProjectMenuItem = projectMenu.Append(wx.ID_ANY, "Open Project...", "Open an existing project")
        saveProjectMenuItem = projectMenu.Append(wx.ID_ANY, "Save Project", "Save the project")
        saveProjectAsMenuItem = projectMenu.Append(wx.ID_ANY, "Save Project As...", "Save the project as...")
        closeProjectMenuItem = projectMenu.Append(wx.ID_ANY, "Close Project", "Close the project")
        preferencesMenuItem = optionsMenu.Append(wx.ID_ANY, "Preferences...\tCtrl+P", "hide preferences")
        runMenuItem = runMenu.Append(wx.ID_ANY, "Run\tF9", "Runs the project")
        generateMenuItem = runMenu.Append(wx.ID_ANY, "Generate C file\tF10", "Generate C code from project")
        genAndCompMenuItem = runMenu.Append(wx.ID_ANY, "Generate and compile\tF11",
                                            "Generate and try to compile it with GCC")
        aboutMenuItem = helpMenu.Append(wx.ID_ANY, "About\tCtrl+F1", "Display info about hide")
        menubar.Append(fileMenu, "&File")
        menubar.Append(editMenu, "&Edit")
        menubar.Append(projectMenu, "&Project")
        menubar.Append(optionsMenu, "&Options")
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
        self.Bind(wx.EVT_MENU, self.OnPreferences, preferencesMenuItem)
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
        if self.editor.modified:
            dlg = wx.MessageDialog("File is modified after last save. Should hide save it?",
                                   "Unsaved file", wx.ICON_QUESTION, wx.YES_NO)
            if dlg.ShowModal() == wx.YES:
                self.OnSave(e)
        self.editor.ClearAll()
        self.editor.filename = None
        self.editor.modified = False

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
            f.write(self.editor.GetText().replace('\r', '\r\n'))
            f.close()
            self.editor.modified = False

    def OnSaveAs(self, e):
        dlg = wx.FileDialog(self, message="Save As", wildcard="F4/Helen sources (*.f4)|*.f4",
                            style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_CANCEL:
            return
        fname = dlg.GetPath()
        self.editor.filename = fname
        f = open(fname, 'w')
        f.write(self.editor.GetText().replace('\r', '\r\n'))
        f.close()
        self.editor.modified = False
        dlg.Destroy()

    def OnQuit(self, e):
        cfg = open("config.json", "w")
        json.dump(self.config, cfg)
        self.Close()

    def OnAbout(self, e):
        info = wx.adv.AboutDialogInfo()
        info.SetName("hide")
        info.SetVersion(verstrs)
        info.SetDescription("hide is a F4/Helen IDE (source code editor).\nPowered by wxPython toolkit")
        info.SetCopyright("(C) 2015 hyst329")
        info.SetWebSite("http://github.com/hyst329/hide")
        info.AddDeveloper("hyst329")
        info.AddTranslator("hyst329")
        wx.adv.AboutBox(info)

    def OnTimer(self, e):
        s = "hide - %s%s" % (self.editor.filename, "*" if self.editor.modified else "")
        self.SetTitle(s)

    def OnPreferences(self, e):
        sdlg = SettingsDialog(self)
        sdlg.LoadConfig(self.config)
        sdlg.InitUI()
        sdlg.ShowModal()
        sdlg.Destroy()

    def OnRun(self, e):
        if not self.editor.filename:
            wx.MessageBox("Please save the file first!", "File needs to be saved", wx.ICON_WARNING)
            return
        elif self.editor.modified:
            self.OnSave(e)
        cmd = "%s %s -i" % (self.helpath, self.editor.filename)
        try:
            out = subprocess.check_output(cmd)
            self.output.Clear()
            self.output.SetValue(out)
        except subprocess.CalledProcessError as e:
            wx.MessageBox(str(e), "Error!", wx.ICON_ERROR)

    def OnGenerate(self, e):
        if not self.editor.filename:
            wx.MessageBox("Please save the file first!", "File needs to be saved", wx.ICON_WARNING)
            return
        elif self.editor.modified:
            self.OnSave(e)
        cmd = "%s %s -g" % (self.helpath, self.editor.filename)
        try:
            out = subprocess.check_output(cmd)
            self.output.Clear()
            self.output.SetValue(out)
        except subprocess.CalledProcessError as e:
            wx.MessageBox(str(e), "Error!", wx.ICON_ERROR)

    def OnGenAndComp(self, e):
        if not self.editor.filename:
            wx.MessageBox("Please save the file first!", "File needs to be saved", wx.ICON_WARNING)
            return
        elif self.editor.modified:
            self.OnSave(e)
        cmd = "%s %s -gc" % (self.helpath, self.editor.filename)
        try:
            out = subprocess.check_output(cmd)
            self.output.Clear()
            self.output.SetValue(out)
        except subprocess.CalledProcessError as e:
            wx.MessageBox(str(e), "Error!", wx.ICON_ERROR)


if __name__ == '__main__':
    app = wx.App()
    MainIDEFrame(None, title='hide')
    app.MainLoop()

