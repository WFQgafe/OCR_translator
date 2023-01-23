import wx

# class Frame(wx.Frame):
#
#     def __init__(self):  # ,pos=(0,0)
#         wx.Frame.__init__(self, None, title=u"", pos=(10, 10), size=(1340, 670),
#                           style=wx.SIMPLE_BORDER | wx.TRANSPARENT_WINDOW)
#         self.Center(wx.CURSOR_WAIT)
#         self.SetMaxSize((1340, 670))
#         self.SetMinSize((1340, 670))
#         self.panel = wx.Panel(self, size=(1340, 670))
#         self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
#
#         Close_Button = wx.Button(self.panel, label=u"关闭", pos=(1240, 0), size=(100, 45))
#
#         self.Bind(wx.EVT_BUTTON, self.OnClose, Close_Button)
#
#     def OnClose(self, event):
#         self.Destroy()
#
#
# if __name__ == "__main__":
#     app = wx.App()
#     frame = Frame()
#     frame.Show()
#     app.MainLoop()



class Trans(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(700, 500), style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)
        self.Text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.HSCROLL)
        self.Text.SetBackgroundColour('Black'), self.Text.SetForegroundColour('White')
        self.SetTransparent(150)  # 设置透明
        self.Show()

    def init_ui(self):
        panel = wx.Panel(self, id=-1, pos=(0, 0), size=(10, 500), style=wx.NO_BORDER)
        # 键盘按下事件
        panel.Bind(wx.EVT_KEY_DOWN, self.key_down)
        self.SetSize(1000, 500)
        self.Centre()
        self.Show(True)

    def key_down(self, e):
        print(e)
        key_code = e.GetKeyCode()
        if key_code == wx.WXK_ESCAPE:
            self.Close()  # 关闭窗口
        else:
            print("按了%s键" % key_code)

class Test(wx.App):
    def OnInit(self):
        self.frame = wx.Frame(parent=None, title='Spare')
        self.frame.SetTransparent(100)
        return True


app = wx.App()
Trans(None, 1, "Translator_WFQ_ver0.1")
app.MainLoop()