import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class frame_programmer:
    def __init__(self, parent):
        self._parent = parent
        self._frame = tk.Frame(self._parent, bg="gray")

        self._frame.grid_rowconfigure(0, weight=1)
        self._frame.grid_rowconfigure(1, weight=1)
        self._frame.grid_rowconfigure(2, weight=1)
        self._frame.grid_columnconfigure(0, weight=1)
        self._frame.grid_columnconfigure(1, weight=1)
        self._frame.grid_columnconfigure(2, weight=1)

        self.online_list = ["v0.1.0", "v0.2.0", "v0.3.0"]
        self.load_online_firmware_combobox = ttk.Combobox(
            self._frame, values=self.online_list, state="readonly")
        self.load_online_firmware_combobox.grid(
            row=1, column=0, padx=5, pady=5)
        self.load_online_combobox_set_default()

        button2 = tk.Button(
            self._frame, text="Load Local Firmware", command=self.select_local_file)
        button2.grid(row=1, column=1, padx=5, pady=5)

        button3 = tk.Button(self._frame, text="Update")
        button3.grid(row=1, column=2, padx=5, pady=5)

    def frame(self):
        return self._frame

    def load_online_combobox_set_default(self):
        self.load_online_firmware_combobox.set("Load Online Fiwmare")

    def load_online_combobox_update_values(self, new_online_list):
        self.online_list = new_online_list
        self.load_online_firmware_combobox.configure(values=self.online_list)

    def select_local_file(self):
        filetypes = (("Bin files", "*.bin"), ("All files", "*.*"))
        self.local_file_path = filedialog.askopenfilename(
            initialdir=".", title="select a firmware", filetypes=filetypes)
        if self.local_file_path:
            print("Selected file:", self.local_file_path)
            self.load_online_combobox_set_default()
        else:
            print("No file selected")
