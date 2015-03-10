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
)
types = (
    # Basic types
    'int',
    'real',
    'logical',
    'char',
    'string',
)
operations = (
    # Basic operations
    'in',
    'out',
    'debugvar',
    'resize',
    'size'
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
        self.STYLE_TYPE = 2
        self.STYLE_OPERATION = 3

        self.StyleSetSpec(self.STYLE_KEYWORD, "fore:#0080FF")
        self.StyleSetSpec(self.STYLE_TYPE, "fore:#008080")
        self.StyleSetSpec(self.STYLE_OPERATION, "fore:#FF8000")
        self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, "size:%d" % 10)
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT, "fore:#0000FF")
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD, "fore:#FF0000")

        self.Bind(wx.stc.EVT_STC_CHANGE, self.onChanged)
        self.Bind(wx.stc.EVT_STC_CHARADDED, self.onCharAdded)

    def coloriseWord(self, styled_text, style):
        text = self.GetText()

        pos = text.find(styled_text)
        while pos != -1:
            nextsym = text[pos + len(styled_text): pos + len(styled_text) + 1]
            prevsym = text[pos - 1: pos]

            if (pos == 0 or not prevsym.isalnum()) and (pos == len(text) - len(styled_text) or not nextsym.isalnum()):
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
        for t in types:
            self.coloriseWord(t, self.STYLE_TYPE)
        for op in operations:
            self.coloriseWord(op, self.STYLE_OPERATION)


    def onCharAdded(self, event):
        key_val = event.GetKey()
        if key_val > 127:
            return

        key = chr(key_val)
        _open = "{(["
        _close = "})]"

        keyindex = _open.find(key)

        if keyindex != -1:
            pos = self.GetCurrentPos()
            text = self.GetText()

            self.AddText(_close[keyindex])
            self.GotoPos(pos)

        if key == "\n":
            pos = self.GetCurrentPos()
            lineno = self.GetCurrentLine()
            line = self.GetLine(lineno - 1)
            line = line.strip()
            for w in ("if", "loop", "fun"):
                if len(line) > len(w) and line[0:len(w)] == w and not line[len(w)].isalnum():
                    self.AddText("\nend" + w)
                    self.GotoPos(pos)
                    pass