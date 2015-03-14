import wx

__author__ = 'tram'


class SettingsDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(SettingsDialog, self).__init__(*args, **kw)
        self.SetSize((300, 200))
        self.SetTitle("Preferences")

    def LoadConfig(self, cfg):
        self.config = cfg

    def InitUI(self):
        self.panel = wx.Panel(self)
        self.grid = wx.GridSizer(2, 2, 5, 5)
        self.labelPath = wx.StaticText(self, label="f4main path: ")
        self.textCtrlPath = wx.TextCtrl(self)
        self.buttonOk = wx.Button(self, label="OK")
        self.buttonCancel = wx.Button(self, label="Cancel")
        self.grid.Add(self.labelPath, 0, wx.EXPAND)
        self.grid.Add(self.textCtrlPath, 0, wx.EXPAND)
        self.grid.Add(self.buttonOk, 0, wx.EXPAND)
        self.grid.Add(self.buttonCancel, 0, wx.EXPAND)
        self.textCtrlPath.SetValue(self.config["helpath"])

        self.buttonOk.Bind(wx.EVT_BUTTON, self.OnOk)
        self.buttonCancel.Bind(wx.EVT_BUTTON, self.OnCancel)

        self.SetSizer(self.grid)
        self.grid.Fit(self)

    def OnOk(self, e):
        self.config["helpath"] = self.textCtrlPath.GetValue()
        self.Destroy()

    def OnCancel(self, e):
        self.Destroy()