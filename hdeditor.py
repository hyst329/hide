import codecs
import wx
import wx.stc

keywords = (
    'if',
    'else',
    'endif',
    'fun',
    'endfun',
    'loop',
    'endloop',
    'return',
    'use',
    'resize',
    # Basic types
    'int',
    'real',
    'logical',
    'char',
    'string',
    # Basic operations
    'in',
    'out',
    'debugvar'
)

class HideEditor(wx.stc.StyledTextCtrl):
    def __init__(self, parent, id=wx.ID_ANY,
                 pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=0,
                 name="editor"):
        wx.stc.StyledTextCtrl.__init__(self, parent, id, pos, size, style, name)
        self.encoder = codecs.getencoder("utf-8")

        font = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_NORMAL, False, 'Fixedsys',
                       wx.FONTENCODING_CP1252)
        for i in range(32):
            self.StyleSetFont(i, font)

        self.STYLE_KEYWORD = 1

        self.StyleSetSpec(self.STYLE_KEYWORD, "fore:#800000")
        self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, "size:%d" % 10)
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT, "fore:#0000FF")
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD, "fore:#FF0000")

        self.Bind(wx.stc.EVT_STC_CHANGE, self.onChanged)

    def coloriseWord(self, styled_text, style):
        text = self.GetText()

        pos = text.find(styled_text)
        while pos != -1:
            nextsym = text[pos + len(styled_text): pos + len(styled_text) + 1]
            prevsym = text[pos - 1: pos]

            if (pos == 0 or prevsym.isspace()) and (pos == len(text) - len(styled_text) or nextsym.isspace()):
                bytepos = self.calcBytePos(text, pos)
                text_byte_len = self.calcByteLen(styled_text)
                self.StartStyling(bytepos, 0xff)
                self.SetStyling(text_byte_len, style)

            pos = text.find(styled_text, pos + len(styled_text))

    def calcByteLen(self, text):
        return len(self.encoder(text)[0])

    def calcBytePos(self, text, pos):
        return len(self.encoder(text[: pos])[0])

    def onChanged(self, event):
        for kw in keywords:
            self.coloriseWord(kw, self.STYLE_KEYWORD)