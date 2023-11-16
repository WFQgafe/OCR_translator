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
import pygetwindow as gw

threadpool = futures.ThreadPoolExecutor(max_workers=1)

chicode = 'ZH'
rect = []
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


def select_window():
    # Get a list of titles of all open windows
    window_titles = [win.title for win in gw.getAllWindows() if win.title]  # Ensure title is not empty
    # Create a dialog to let the user select a window
    dlg = wx.SingleChoiceDialog(None, "Select a window to capture:", "Choose Window", window_titles)

    if dlg.ShowModal() == wx.ID_OK:
        selected_title = dlg.GetStringSelection()
    else:
        selected_title = None

    dlg.Destroy()

    return selected_title


class Trans(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(800, 400), style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)
        self.framew,self.frameh = self.GetSize()
        self.isDragging = False
        self.text = wx.TextCtrl(self,size=(self.framew-50,self.frameh-20),
                                style=wx.TE_RICH | wx.TE_READONLY | wx.TE_MULTILINE  | wx.BRUSHSTYLE_TRANSPARENT | wx.LEFT | wx.TE_BESTWRAP | wx.BORDER_NONE) # text setting
        self.SetBackgroundColour("BLACK")
        self.text.SetBackgroundColour("BLack")
        self.text.SetFont(wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL, False, u'Consolas'))
        self.text.SetForegroundColour("White")

        self.set_range_button = wx.Button(self, label="Set range", pos=(self.framew - 100, self.frameh - 120)) # set range button
        self.set_range_button.Bind(wx.EVT_BUTTON, self.OnClicked)

        self.select_window_button = wx.Button(self, label="Select window", pos=(self.framew - 240, self.frameh - 120))
        self.Bind(wx.EVT_BUTTON, self.on_select_window, self.select_window_button)

        self.Bind(wx.EVT_SIZE, self.Sizechange)

        self.SetTransparent(500)  # transparency of windows

        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.toggle = wx.ToggleButton(self, label="Translate now", pos=(self.framew-300,self.frameh-120)) # translate toggle button
        self.Bind(wx.EVT_TOGGLEBUTTON, self.TransClicking)


    def OnClicked(self, event):
        """Start the range setting process."""
        # self.SetWindowStyleFlag(self.GetWindowStyleFlag() & ~wx.STAY_ON_TOP)
        self.set_range_button.SetLabel("Setting...")
        self.start_global_mouse_listener()

    def start_global_mouse_listener(self):
        self.listener = mo.Listener(on_click=self.global_mouse_click)
        self.listener.start()

    def global_mouse_click(self, x, y, button, pressed):
        if pressed:
            if not self.isDragging:
                self.isDragging = True
                self.startPos = wx.Point(x, y)
            else:
                self.isDragging = False
                self.endPos = wx.Point(x, y)
                self.calculate_rect()
                self.listener.stop()
        self.Refresh()


    def calculate_rect(self):
        topLeftX = min(self.startPos.x, self.endPos.x)
        topLeftY = min(self.startPos.y, self.endPos.y)
        bottomRightX = max(self.startPos.x, self.endPos.x)
        bottomRightY = max(self.startPos.y, self.endPos.y)
        global rect
        rect = (topLeftX, topLeftY, bottomRightX - topLeftX, bottomRightY - topLeftY)
        self.set_range_button.SetLabel("Set range")  # Reset the button label

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        if self.isDragging or hasattr(self, 'endPos'):
            # If dragging or if the rectangle has been finalized
            rect = wx.Rect(self.startPos, self.endPos if hasattr(self, 'endPos') else self.currentPos)
            dc.SetPen(wx.Pen("BLACK", 2))  # Black border
            dc.SetBrush(wx.Brush("WHITE", style=wx.BRUSHSTYLE_TRANSPARENT))  # Transparent fill
            dc.DrawRectangle(rect)

    def translating_thread(self):
        thread1 = threading.currentThread()
        while getattr(thread1, "do_run", True):
            self.text.SetValue(translator(self,self.selected_window_title))
            time.sleep(0.5)

    def on_select_window(self, event):
        self.selected_window_title = select_window()
        if self.selected_window_title:
            wx.MessageBox(f'Selected Window: {self.selected_window_title}', 'Info', wx.OK | wx.ICON_INFORMATION)

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
            wx.CallAfter(self.set_label, "Translate now")

    def Sizechange(self,event):
        self.framew,self.frameh = self.GetSize()
        self.text.SetSize(self.framew-20,self.frameh-100)
        self.select_window_button.SetPosition(((20, self.frameh - 80)))
        self.set_range_button.SetPosition((160, self.frameh - 80))
        self.toggle.SetPosition((260, self.frameh-80))
        self.Refresh()


def __init__(self):
        super().__init__()
        self.text = QtWidgets.QLabel("Getiing start",
                                     alignment=QtCore.Qt.AlignCenter)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)

def capture_window(title):
    # Find the window by its title
    try:
        window = gw.getWindowsWithTitle(title)[0]
    except IndexError:
        # If the window isn't found, return None
        return None

    current_active = [win for win in gw.getWindowsWithTitle("Translator_WFQ_ver0.3") if win.title][0]
    current_active.minimize()
    window = [win for win in gw.getWindowsWithTitle(title) if win.title][0]
    window.activate()
    intersect_left = max(window.left, rect[0])
    intersect_top = max(window.top, rect[1])
    intersect_right = min(window.left + window.width, rect[0] + rect[2])
    intersect_bottom = min(window.top + window.height, rect[1] + rect[3])
    if intersect_left < intersect_right and intersect_top < intersect_bottom:
        screenshot = gui.screenshot(
            region=(intersect_left, intersect_top, intersect_right - intersect_left, intersect_bottom - intersect_top))
    else:
        return "No intersection between set range and window"
    screenshot.save('pic.jpg')

    current_active.restore()
    current_active.activate()


def translator(window_instance,title_of_window_to_capture):
    # Remove the "always on top" flag
    window_instance.SetWindowStyleFlag(window_instance.GetWindowStyleFlag() & ~wx.STAY_ON_TOP)
    reader = easyocr.Reader(['ja', 'en'])
    capture_window(title_of_window_to_capture)
    # Restore the "always on top" flag
    window_instance.SetWindowStyleFlag(window_instance.GetWindowStyleFlag() | wx.STAY_ON_TOP)
    result = reader.readtext('pic.jpg', detail=0, paragraph=True)
    print(result)
    translator = deepl.Translator(deeplauth)
    trans = translator.translate_text(text=str(result), target_lang=chicode)
    return str(trans)


app = wx.App()
Trans(None, 1, "Translator_WFQ_ver0.3").Show()
app.MainLoop()







