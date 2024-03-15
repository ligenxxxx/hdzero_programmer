import sys
import os

import tkinter as tk
from tkinter import ttk

from frame_vtx import frame_vtx
from frame_hybrid_view import frame_hybrid_viewer
from frame_event_vrx import frame_event_vrx
from frame_programmer import frame_programmer
from frame_statusbar import frame_statusbar

from download import *
from parse_file import *
import global_var
from global_var import *
from ch341 import my_ch341
import base64
from icon32 import icon32
import io
class MyGUI:

    def __init__(self, init_window_name):
        self.winWidth = 640
        self.winHeight = 320    #280
        self.title = "HDZero Programmer"

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
        self._main_window.geometry("%sx%s+%s+%s" %(self.winWidth, self.winHeight, x, y))
        self._main_window.resizable(False, False)
        
        icon_base64 = base64.b64decode(icon32)
        icon_bytes = io.BytesIO(icon_base64)
        icon = tk.PhotoImage(data=icon_bytes.getvalue())
        
        self._main_window.iconphoto(True, icon)


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
        self._programmer_frame.local_fw_button["command"] = self.on_load_local_firmware
        self._programmer_frame.update_button["command"] = self.on_update

    def init_vtx_frame(self):
        self._vtx_frame = frame_vtx(self._tabCtrl)
        self._vtx_frame.target_combobox.bind("<<ComboboxSelected>>", self.on_select_vtx_target)

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

        self._statusbar_frame.status_label_set_text("FW: Online")

    def on_load_local_firmware(self):
        self._programmer_frame.select_local_file()
        fw_size = os.path.getsize(self._programmer_frame.local_file_path)

        if self.current_selected_tab() == 0:
            if fw_size == 0 or fw_size >= 65536:
                self._statusbar_frame.status_label_set_text("FW: Warning Firmware Size")
            elif self._programmer_frame.mode == 1:
                self._statusbar_frame.status_label_set_text("FW: Local")
                self._programmer_frame.update_button_enable()
              
        elif self.current_selected_tab() == 1:
            self._statusbar_frame.status_label_set_text("FW: Local")
            self._programmer_frame.update_button_enable()        
            self._programmer_frame.mode = 1
            my_ch341.fw_path = self._programmer_frame.local_file_path
            my_ch341.status = ch341_status.HYBRIDVIEW_GET_FW.value
            
        elif self.current_selected_tab() == 2:
            self._statusbar_frame.status_label_set_text("FW: Local")
            self._programmer_frame.update_button_enable()        
            self._programmer_frame.mode = 1
            my_ch341.fw_path = self._programmer_frame.local_file_path
            my_ch341.status = ch341_status.EVENTVRX_GET_FW.value
   
    def on_update(self):
        if my_ch341.connect_hybridview(0) == 1:
            self._programmer_frame.version_combobox_disable()
            self._programmer_frame.local_fw_button_disable()
            self._programmer_frame.update_button_disable()
            self._vtx_frame.target_combobox_disable()
            self._hybrid_viewer_frame.setting_disable()

        if self.current_selected_tab() == 0:
            my_ch341.status = ch341_status.VTX_NOTCONNECTED.value  # to connect vtx
            self._statusbar_frame.status_label_set_text("Connecting VTX ...")
            self._statusbar_frame.progress_bar_set_value(1)
            
        elif self.current_selected_tab() == 1:
            if my_ch341.connect_hybridview(0) == 1:
                self._statusbar_frame.status_label_set_text("Updating HybridView ...")
                self._statusbar_frame.progress_bar_set_value(1)
                my_ch341.status = ch341_status.HYBRIDVIEW_UPDATE.value
                
        elif self.current_selected_tab() == 2:
            if my_ch341.connect_eventvrx() == 1:
                self._statusbar_frame.status_label_set_text("Updating EventVRX ...")
                self._statusbar_frame.progress_bar_set_value(1)
                my_ch341.status = ch341_status.EVENTVRX_UPDATE.value

    def version_selection_disable(self):
        self._programmer_frame.version_combobox.config(state="disabled")

    def version_selection_enable(self):
        self._programmer_frame.version_combobox.config(state="readonly")

    def update_button_disable(self):
        self._programmer_frame.update_button.config(state="disabled")

    def update_button_enable(self):
        self._programmer_frame.update_button.config(state="normal")            
            
    def on_tab_changed(self, event):
        print("Selected tab:", self.current_selected_tab())
        self._programmer_frame.version_combobox_update_values("")
        self._programmer_frame.version_combobox_set_default()
        self._programmer_frame.update_button_disable()

        if self.current_selected_tab() == 0:
            self._vtx_frame.target_combobox_set_default()
            self._programmer_frame.version_combobox_disable()
            self._programmer_frame.local_fw_button_disable()
        elif self.current_selected_tab() == 1:
            my_ch341.status = ch341_status.HYBRIDVIEW_NOTCONNECTED.value   # to connect HybridView
        elif self.current_selected_tab() == 2:
            my_ch341.status = ch341_status.EVENTVRX_NOTCONNECTED.value     # to connect eventvrx
        
    def current_selected_tab(self):
        return self._tabCtrl.index(self._tabCtrl.select())

    def refresh(self):
        '''
        1. update vtx
        -   press update button
        -   connect vtx
        -   wait until vtx is connected
        -   download fw if use online fw
        -   wait until download is done if use online fw
        -   write vtx id & fw to flash
        -   wait until write done
        
        2. update hybrid view
        -
        -
        3. update event vrx
        '''
        if my_download.status == download_status.FILE_PARSE.value:
            my_parse.parse_vtx_common()
            my_parse.parse_vtx_releases()
            my_download.status = download_status.IDLE.value
            self._vtx_frame.target_combobox_update_value(list(my_parse.vtx_info.keys()))
            self._vtx_frame.target_combobox_set_default()
            self._vtx_frame.target_combobox_enable()
            self._statusbar_frame.status_label_set_text(" ")
        elif my_download.status == download_status.DOWNLOAD_VTX_FW_DONE.value:
            my_download.status = download_status.IDLE.value
            selected_target = self._vtx_frame.target_combobox.get()
            my_ch341.target_id = my_parse.vtx_info[selected_target]["id"]
            my_ch341.fw_path = my_download.save_path
            my_ch341.written_len = 0
            my_ch341.status = ch341_status.VTX_UPDATE.value
            self._statusbar_frame.status_label_set_text("Updating VTX ...")

        if my_ch341.status == ch341_status.VTX_CONNECTED.value:  # vtx is connected
            my_ch341.status = ch341_status.IDLE.value
            if self._programmer_frame.mode == 0:
                my_download.url = self._programmer_frame.url
                my_download.save_path = "FW"
                my_download.status = download_status.DOWNLOAD_VTX_FW.value  # download url
                self._statusbar_frame.status_label_set_text("Download Firmware ...")
            else:
                selected_target = self._vtx_frame.target_combobox.get()
                my_ch341.target_id = my_parse.vtx_info[selected_target]["id"]
                my_ch341.fw_path = self._programmer_frame.local_file_path
                my_ch341.status = ch341_status.VTX_UPDATE.value
        elif my_ch341.status == ch341_status.VTX_UPDATE.value:  # refresh progress bar
            value = (my_ch341.written_len / my_ch341.to_write_len * 100) % 101
            self._statusbar_frame.progress_bar_set_value(value)

        elif my_ch341.status == ch341_status.VTX_UPDATEDONE.value:  # vtx update done
            self._statusbar_frame.progress_bar_set_value(100)
            self._programmer_frame.version_combobox_enable()
            self._programmer_frame.local_fw_button_enable()
            self._vtx_frame.target_combobox_enable()
            self._programmer_frame.update_button_disable()
            self._statusbar_frame.status_label_set_text("Update VTX Done")
            my_ch341.status = ch341_status.IDLE.value
            
        # ------------ HybridView ---------------
        elif my_ch341.status == ch341_status.HYBRIDVIEW_NOTCONNECTED.value:
            if my_ch341.connect_hybridview(0) == 0:
                self._hybrid_viewer_frame.setting_disable()

        elif my_ch341.status == ch341_status.HYBRIDVIEW_CONNECTED.value:  # HybridView is connected
            if self.current_selected_tab() == 1:
                if my_ch341.hybridview_connected == 1 and my_ch341.read_setting_flag == 1:
                    self._hybrid_viewer_frame.setting_enable()
                    my_gui.version_selection_enable()
                    self._programmer_frame.local_fw_button_enable()
                    my_ch341.read_setting()
                    self._hybrid_viewer_frame.write_setting(global_var.brightness, global_var.contrast, global_var.saturation, 
                        global_var.backlight, global_var.cell_count, global_var.warning_cell_voltage)
                    my_ch341.read_setting_flag = 0
                else:
                    if my_ch341.connect_hybridview(0) == 0:
                        self._hybrid_viewer_frame.setting_disable()                    
                        my_gui.version_selection_disable()
                        self._programmer_frame.local_fw_button_disable()
                        my_ch341.hybridview_connected = 0
                        my_ch341.status = ch341_status.HYBRIDVIEW_NOTCONNECTED.value
                        my_ch341.read_setting_flag = 1
                                    
                self._hybrid_viewer_frame.usb_heart()
                
        elif my_ch341.status == ch341_status.HYBRIDVIEW_UPDATE.value:  # refresh progress bar
            value = (my_ch341.written_len / my_ch341.to_write_len * 100) % 101
            print("progress_bar_value: ", value)
            self._statusbar_frame.progress_bar_set_value(value)

        elif my_ch341.status == ch341_status.HYBRIDVIEW_UPDATEDONE.value:  # HybridView update done
            self._statusbar_frame.progress_bar_set_value(100)
            self._programmer_frame.version_combobox_enable()
            self._programmer_frame.local_fw_button_enable()
            self._vtx_frame.target_combobox_enable()
            self._programmer_frame.update_button_disable()
            self._statusbar_frame.status_label_set_text("Update HybridView Done")            
            my_ch341.status = ch341_status.IDLE.value

        # --------------------- eventvrx -------------------------------
        elif my_ch341.status == ch341_status.EVENTVRX_NOTCONNECTED.value:
            if my_ch341.connect_eventvrx() == 0:
                my_gui.version_selection_disable()
                self._programmer_frame.local_fw_button_disable()

        elif my_ch341.status == ch341_status.EVENTVRX_CONNECTED.value:  # eventvrx is connected
            if self.current_selected_tab() == 2:
                if my_ch341.eventvrx_connected == 1:
                    my_gui.version_selection_enable()
                    self._programmer_frame.local_fw_button_enable()
                else:
                    if my_ch341.connect_eventvrx() == 0:
                        my_gui.version_selection_disable()
                        self._programmer_frame.local_fw_button_disable()
                        my_ch341.eventvrx_connected = 0
                        my_ch341.status = ch341_status.EVENTVRX_NOTCONNECTED.value
                                                    
        elif my_ch341.status == ch341_status.EVENTVRX_UPDATE.value:  # eventvrx refresh progress bar
            value = (my_ch341.written_len / my_ch341.to_write_len * 100) % 101
            #print("progress_bar_value: ", value)
            self._statusbar_frame.progress_bar_set_value(value)

        elif my_ch341.status == ch341_status.EVENTVRX_UPDATEDONE.value:  # eventvrx update done
            self._statusbar_frame.progress_bar_set_value(100)
            self._programmer_frame.version_combobox_enable()
            self._programmer_frame.local_fw_button_enable()
            self._vtx_frame.target_combobox_enable()
            self._programmer_frame.update_button_disable()
            self._statusbar_frame.status_label_set_text("Update EventVRX Done")            
            my_ch341.status = ch341_status.IDLE.value

        self._main_window.after(100, self.refresh)

def on_closing():
    my_download.status = download_status.DOWNLOAD_EXIT.value
    my_ch341.status = ch341_status.STATUS_EXIT.value
    sys.exit()

global my_gui

def ui_thread_proc():
    global my_gui
    root = tk.Tk()

    my_gui = MyGUI(root)
    my_gui.refresh()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    my_gui._main_window.mainloop()