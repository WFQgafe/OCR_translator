import time
import sys
import easyocr
import pyscreenshot
import cv2
import threading
import deepl
import os
import wx
import pynput.mouse as mo
import pyautogui as gui
from concurrent import futures



threadpool = futures.ThreadPoolExecutor(max_workers=1)

japcode = 'ja'
chicode = 'ZH'
L_dis = 200
U_dis = 900
R_dis = 2300
D_dis = 1200
boolean = True
deeplauth="13259c5f-5944-143f-091c-5bcf8c8bbc9a:fx"

startpos=(0,0)
endpos=(0,0)
clickcount=0


def on_click(x, y, button, pressed):
    global clickcount, startpos, endpos
    if pressed:
        clickcount+=1
        if clickcount==1:
            startpos=x,y
        elif clickcount==2:
            endpos=x,y


class Trans(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(300, 300), style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)
        self.framew,self.frameh = self.GetSize()

        self.text = wx.TextCtrl(self,size=(self.framew-50,self.frameh-20),
                                style=wx.TE_RICH | wx.TE_READONLY | wx.TE_MULTILINE  | wx.BRUSHSTYLE_TRANSPARENT | wx.LEFT | wx.TE_BESTWRAP | wx.BORDER_NONE) # text setting
        self.SetBackgroundColour("BLACK")
        self.text.SetBackgroundColour("BLack")
        self.text.SetFont(wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL, False, u'Consolas'))
        self.text.SetForegroundColour("White")


        self.btn = wx.Button(self, label="Set range", pos=(self.framew-200,self.frameh-120)) # set range button
        self.btn.Bind(wx.EVT_BUTTON, self.OnClicked)

        self.Bind(wx.EVT_SIZE, self.Sizechange)

        self.SetTransparent(150)  # transparency of windows

        self.toggle = wx.ToggleButton(self, label="Translate Now", pos=(self.framew-300,self.frameh-120)) # translate toggle button
        self.Bind(wx.EVT_TOGGLEBUTTON, self.TransClicking)


    def translating_thread(self):
        thread1 = threading.currentThread()
        while getattr(thread1, "do_run", True):
            self.text.SetValue(translator())
            time.sleep(0.5)




    def TransClicking(self, event):
        state = event.GetEventObject()
        threadpool.submit(self.blocking, state)


    def set_label(self, text):
        self.toggle.SetLabel(text)


    def blocking(self, state):
        if state.GetValue() == True:
            wx.CallAfter(self.set_label, "Translating...")
            thread1 = threading.Thread(target=self.translating_thread, daemon=True)
            thread1.start()

        while state.GetValue() == True:
            continue

        else:
            thread1.do_run = False
            wx.CallAfter(self.set_label, "Translate Now")



    def OnClicked(self,event):
        self.btn.SetLabel("Setting...")
        global clickcount, L_dis, U_dis, R_dis, D_dis
        listener = mo.Listener(on_click=on_click)
        clickcount = 0
        listener.start()
        while True:
            if clickcount>=2:
                listener.stop()
                self.btn.SetLabel("Set range")
                break
        w,h = gui.size()
        L_dis=startpos[0]
        U_dis=startpos[1]
        R_dis=endpos[0]
        D_dis=endpos[1]


    def Sizechange(self,event):
        self.framew,self.frameh = self.GetSize()
        self.text.SetSize(self.framew-20,self.frameh-100)
        self.btn.SetPosition((20, self.frameh - 80))
        self.toggle.SetPosition((120, self.frameh-80))
        self.Refresh()


def __init__(self):
        super().__init__()
        self.text = QtWidgets.QLabel("Getiing start",
                                     alignment=QtCore.Qt.AlignCenter)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)


def translator():
    reader = easyocr.Reader([japcode])
    print(L_dis,U_dis,R_dis,D_dis)
    pic_region = pyscreenshot.grab(bbox=(L_dis, U_dis, R_dis, D_dis))
    pic_region.save('pic.jpg')
    result = reader.readtext('pic.jpg', detail=0, paragraph=True)
    translator = deepl.Translator(deeplauth)
    trans = translator.translate_text(text=str(result), target_lang=chicode)
    return str(trans)


app = wx.App()
Trans(None, 1, "Translator_WFQ_ver0.1").Show()
app.MainLoop()







