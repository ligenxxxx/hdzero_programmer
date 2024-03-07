import tkinter as tk
from tkinter import ttk


class frame_vtx():
    def __init__(self, parent):
        self._parent = parent
        self._frame = tk.Frame(parent)
        parent.add(self._frame, text="VTX")

        self.target_list = []

        self._frame.grid_rowconfigure(0, weight=1)
        self._frame.grid_rowconfigure(1, weight=1)
        self._frame.grid_rowconfigure(2, weight=1)
        self._frame.grid_columnconfigure(0, weight=1)
        self._frame.grid_columnconfigure(1, weight=1)
        self._frame.grid_columnconfigure(2, weight=1)

        self.target_combobox = tk.ttk.Combobox(
            self._frame, values=self.target_list, state="readonly")
        self.target_combobox.grid(
            row=1, column=1, padx=5, pady=5)
        self.target_combobox_set_default()
        self.target_combobox_disable()

    def frame(self):
        return self._frame

    def target_combobox_set_default(self):
        self.target_combobox.set("Choose a VTX")

    def target_combobox_disable(self):
        self.target_combobox.configure(state="disabled")

    def target_combobox_enable(self):
        self.target_combobox.configure(state="readonly")

    def target_combobox_update_value(self, new_values):
        self.target_combobox.configure(values=new_values)
