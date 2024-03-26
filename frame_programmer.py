import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class frame_programmer:
    def __init__(self, parent):
        self._parent = parent
        self._frame = tk.Frame(self._parent)

        self._frame.grid_rowconfigure(0, weight=1)
        self._frame.grid_rowconfigure(1, weight=1)
        self._frame.grid_rowconfigure(2, weight=1)
        self._frame.grid_columnconfigure(0, weight=1)
        self._frame.grid_columnconfigure(1, weight=1)
        self._frame.grid_columnconfigure(2, weight=1)

        self.online_list = []
        self.mode = 0  # 0/1 : url/local path
        self.local_file_path = ""
        self.url = ""
        
        self.is_load_online = tk.StringVar()

        self.version_combobox = ttk.Combobox(
            self._frame, values=self.online_list, state="readonly")
        self.version_combobox_set_default()
        self.version_combobox_disable()
        
        self.online_fw_button = ttk.Radiobutton(self._frame, text="Load Online Firmware", variable=self.is_load_online, value='1')
        self.online_fw_button_show()
        self.online_fw_button_disable()


        self.local_fw_button = ttk.Radiobutton(self._frame, text="Load Local Firmware", variable=self.is_load_online, value='0')
        self.local_fw_button.grid(row=1, column=1, padx=5, pady=5)
        self.local_fw_button_disable()

        self.update_button = tk.Button(self._frame, text="Update")
        self.update_button.grid(row=1, column=2, padx=5, pady=5)
        self.update_button_disable()

    def frame(self):
        return self._frame

    def version_combobox_set_default(self):
        self.version_combobox.set("Load Online Fiwmare")

    def version_combobox_disable(self):
        self.version_combobox["state"] = "disabled"

    def version_combobox_enable(self):
        self.version_combobox["state"] = "readonly"

    def version_combobox_update_values(self, new_values):
        self.online_list = new_values
        self.version_combobox.configure(values=self.online_list)

    def online_fw_button_disable(self):
        self.online_fw_button.config(state="disabled")

    def online_fw_button_enable(self):
        self.online_fw_button.config(state="normal")
    
    def online_fw_button_show(self):
        self.online_fw_button.grid(row=1, column=0, padx=5, pady=5)
        self.version_combobox.grid_remove()
    
    def online_fw_button_hidden(self):
        self.version_combobox.grid(
            row=1, column=0, padx=5, pady=5)
        self.online_fw_button.grid_remove()

    def local_fw_button_disable(self):
        self.local_fw_button.config(state="disabled")

    def local_fw_button_enable(self):
        self.local_fw_button.config(state="normal")
    
    def deselect(self):
        self.is_load_online.set("")

    def select_local_file(self):
        self.version_combobox_set_default()
        filetypes = (("Bin files", "*.bin"), ("All files", "*.*"))
        try:
            self.local_file_path = filedialog.askopenfilename(
                initialdir=".", title="select a firmware", filetypes=filetypes)
        except:
            print("please select a firmware file")

        if self.local_file_path:
            self.mode = 1

    def update_button_disable(self):
        self.update_button["state"] = "disabled"

    def update_button_enable(self):
        self.update_button["state"] = "normal"
