import tkinter as tk
from tkinter import ttk
import sys


from frame_vtx import frame_vtx
from frame_hybrid_viewer import frame_hybrid_viewer
from frame_event_vrx import frame_event_vrx
from frame_programmer import frame_programmer
from frame_statusbar import frame_statusbar

from ch341 import my_ch341

from download import *
from parse_file import *


class MyGUI:

    def __init__(self, init_window_name):
        self.winWidth = 640
        self.winHeight = 280
        self.title = "HDZero Programmer v0.0.1"

        self._programmer_frame = None

        self._main_window = init_window_name
        self._main_window.grid_rowconfigure(0, weight=8)
        self._main_window.grid_rowconfigure(1, weight=2)
        self._main_window.grid_rowconfigure(2, weight=1)
        self._main_window.grid_columnconfigure(0, weight=1)

        self.init_tab()
        self.init_programmer()
        self._programmer_frame.frame().grid(row=1, column=0, sticky="nsew")
        
        self.init_statusbar()
        self._statusbar_frame.frame().grid(row=2, column=0, sticky="nsew")

    def init_main_window(self):
        screenWidth = self._main_window.winfo_screenwidth()
        screenHeight = self._main_window.winfo_screenheight()
        x = int((screenWidth - self.winWidth) / 2)
        y = int((screenHeight - self.winHeight) / 2)

        self._main_window.title(self.title)
        self._main_window.geometry("%sx%s+%s+%s" %
                                   (self.winWidth, self.winHeight, x, y))
        self._main_window.resizable(False, False)

    def init_tab(self):
        self._tabCtrl = ttk.Notebook(self._main_window)
        self.init_main_window()
        self.init_vtx_frame()
        self.init_hybrid_viewer_frame()
        self.init_event_vrx_frame()
        self._tabCtrl.select(self._vtx_frame.frame())
        self._tabCtrl.grid(row=0, column=0, sticky="nsew")
        self._tabCtrl.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def init_programmer(self):
        self._programmer_frame = frame_programmer(self._main_window)
        self._programmer_frame.version_combobox.bind(
            "<<ComboboxSelected>>",  self.on_select_version)
        self._programmer_frame.update_button["command"] = self.on_update

    def init_vtx_frame(self):
        self._vtx_frame = frame_vtx(self._tabCtrl)
        self._vtx_frame.target_combobox.bind(
            "<<ComboboxSelected>>", self.on_select_vtx_target)

    def init_hybrid_viewer_frame(self):
        self._hybrid_viewer_frame = frame_hybrid_viewer(self._tabCtrl)

    def init_event_vrx_frame(self):
        self._event_vrx_frame = frame_event_vrx(self._tabCtrl)
        
    def init_statusbar(self):
        self._statusbar_frame = frame_statusbar(self._main_window)

    def on_select_vtx_target(self, event):
        selected_target = self._vtx_frame.target_combobox.get()
        print("Selected target:", selected_target)
        version_list = list(my_parse.vtx_info[selected_target].keys())[1:]
        self._programmer_frame.version_combobox_update_values(version_list)
        self._programmer_frame.version_combobox_set_default()
        self._programmer_frame.version_combobox_enable()
        self._programmer_frame.local_fw_button_enable()

    def on_select_version(self, event):
        selected_version = self._programmer_frame.version_combobox.get()
        print("Selected:", selected_version)
        self._programmer_frame.mode = 0

        if self.current_selected_tab() == 0:
            self._programmer_frame.update_button_enable()
            self._programmer_frame.url = my_parse.vtx_info[self._vtx_frame.target_combobox.get(
            )][self._programmer_frame.version_combobox.get()]
            print("FW:", self._programmer_frame.url)

    def on_update(self):
        self._programmer_frame.version_combobox_disable()
        self._programmer_frame.local_fw_button_disable()
        self._programmer_frame.update_button_disable()
        print("connecting vtx")
        my_ch341.status = 1  # to connect vtx

    def on_tab_changed(self, event):
        print("Selected tab:", self.current_selected_tab())
        self._programmer_frame.version_combobox_update_values("")
        self._programmer_frame.version_combobox_set_default()
        self._programmer_frame.update_button_disable()
        if self.current_selected_tab() == 0:
            self._vtx_frame.target_combobox_set_default()
            self._programmer_frame.version_combobox_disable()
            self._programmer_frame.local_fw_button_disable()

    def current_selected_tab(self):
        return self._tabCtrl.index(self._tabCtrl.select())

    def refresh(self):
        '''
        - update vtx
        -   press update button
        -   connect vtx
        -   wait until vtx is connected
        -   download fw if use online fw
        -   wait until download is done if use online fw
        -   write vtx id & fw to flash
        -   wait until write done
        '''
        if my_download.status == -1:
            print("parse file")
            my_parse.parse_vtx_common()
            my_parse.parse_vtx_releases()
            my_download.status = 0
            self._vtx_frame.target_combobox_update_value(
                list(my_parse.vtx_info.keys()))
            self._vtx_frame.target_combobox_set_default()
            self._vtx_frame.target_combobox_enable()
            self._statusbar_frame.status_label_set_text(" ")
        elif my_download.status == 2:
            my_download.status = 0
            selected_target = self._vtx_frame.target_combobox.get()
            my_ch341.target_id = my_parse.vtx_info[selected_target]["id"]
            my_ch341.fw_path = my_download.save_path
            my_ch341.status = 3
            print("FW is downloaded, to update vtx")

        if my_ch341.status == 2:  # vtx is connected
            print("vtx found")
            my_ch341.status = 0

            if self._programmer_frame.mode == 0:
                my_download.url = self._programmer_frame.url
                my_download.save_path = "FW"
                my_download.status = 1  # download url
            else:
                selected_target = self._vtx_frame.target_combobox.get()
                my_ch341.target_id = my_parse.vtx_info[selected_target]["id"]
                my_ch341.fw_path = self._programmer_frame.local_file_path
                my_ch341.status = 3
                print("To update vtx")

        elif my_ch341.status == 4:  # update done
            self._programmer_frame.version_combobox_enable()
            self._programmer_frame.local_fw_button_enable()
            self._programmer_frame.update_button_enable()
            my_ch341.status = 0
            print("update done")

        self._main_window.after(100, self.refresh)


def on_closing():
    my_download.status = 255
    my_ch341.status = 255
    sys.exit()


global my_gui


def ui_thread_proc():
    global my_gui
    root = tk.Tk()

    my_gui = MyGUI(root)
    my_gui.refresh()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    my_gui._main_window.mainloop()
