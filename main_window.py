import tkinter as tk
from tkinter import ttk


from frame_vtx import frame_vtx
from frame_hybrid_viewer import frame_hybrid_viewer
from frame_event_vrx import frame_event_vrx
from frame_programmer import frame_programmer


class MyGUI:
    vtx_frame = None
    hybrid_view_vrx_frame = None
    event_vrx_frame = None

    def __init__(self, init_window_name):
        self.winWidth = 640
        self.winHeight = 280
        self.title = "HDZero Programmer v0.0.1"

        self._main_window = init_window_name
        self._main_window.grid_rowconfigure(0, weight=7)
        self._main_window.grid_rowconfigure(1, weight=3)
        self._main_window.grid_columnconfigure(0, weight=1)

        self._tabCtrl = ttk.Notebook(self._main_window)
        self.init_main_window()
        self.init_vtx_frame()
        self.init_hybrid_viewer_frame()
        self.init_event_vrx_frame()
        self._tabCtrl.select(self._vtx_frame.frame())
        self._tabCtrl.grid(row=0, column=0, sticky="nsew")

        self.init_programmer()
        self._programmer_frame.frame().grid(row=1, column=0, sticky="nsew")

    def init_main_window(self):

        screenWidth = self._main_window.winfo_screenwidth()
        screenHeight = self._main_window.winfo_screenheight()
        x = int((screenWidth - self.winWidth) / 2)
        y = int((screenHeight - self.winHeight) / 2)

        self._main_window.title(self.title)
        self._main_window.geometry("%sx%s+%s+%s" %
                                   (self.winWidth, self.winHeight, x, y))
        self._main_window.resizable(False, False)

    def init_vtx_frame(self):
        self._vtx_frame = frame_vtx(self._tabCtrl)

    def init_hybrid_viewer_frame(self):
        self._hybrid_viewer_frame = frame_hybrid_viewer(self._tabCtrl)

    def init_event_vrx_frame(self):
        self._event_vrx_frame = frame_event_vrx(self._tabCtrl)

    def init_programmer(self):
        self._programmer_frame = frame_programmer(self._main_window)


def ui_thread_proc():
    root = tk.Tk()

    my_gui = MyGUI(root)
    my_gui._main_window.mainloop()
